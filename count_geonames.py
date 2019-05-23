import time
import os
import sys
import multiprocessing as mp
import pymongo
from pubcrawler.article import Article
from epitator.annodoc import AnnoDoc
from epitator.annotier import AnnoTier
from epitator.geoname_annotator import GeonameAnnotator

from reporter import Reporter, MongoQueryReporter


def do_work(queue):
    articles = pymongo.MongoClient("localhost", 27017).pmc.articles
    geoname_annotator = GeonameAnnotator()
    for i in iter(queue.get, "STOP"):
        record = articles.find_one(i)
        if len(record["extracted_text"]) > 100000:
            all_geospans = 0
            n_geospans = 0
            geospan_density = 0
        else:
            article = AnnoDoc(record["extracted_text"])
            article.add_tier(geoname_annotator)
            article.tiers.update(
                {"parentheticals": article.create_regex_tier("\(.*?\)")}
            )

            all_geospans = article.tiers["geonames"]
            geospans = AnnoTier(
                [span for span in all_geospans if span.metadata["geoname"].score > 0.13]
            )
            parentheticals = article.tiers["parentheticals"]
            nonparen_geospans = geospans.subtract_overlaps(parentheticals)
            paren_geospans = geospans.subtract_overlaps(nonparen_geospans)

            n_all_geospans = len(all_geospans)
            n_geospans = len(geospans)
            n_nonparen_geospans = len(nonparen_geospans)
            n_paren_geospans = len(paren_geospans)

            geospan_density = n_geospans / len(record["extracted_text"])
            nonparen_geospan_density = n_nonparen_geospans / len(
                record["extracted_text"]
            )
            paren_geospan_density = n_paren_geospans / len(record["extracted_text"])
        articles.update_one(
            i,
            {
                "$set": {
                    "article_meta.n_all_geospans": n_all_geospans,
                    "article_meta.n_geospans": n_geospans,
                    "article_meta.n_nonparen_geospans": n_nonparen_geospans,
                    "article_meta.n_paren_geospans": n_paren_geospans,
                    "article_meta.geospan_density": geospan_density,
                    "article_meta.nonparen_geospan_density": nonparen_geospan_density,
                    "article_meta.paren_geospan_density": paren_geospan_density,
                }
            },
        )
        record = articles.find_one(i)


def report_work(interval, query):
    print("Started!", flush=True)
    articles = pymongo.MongoClient("localhost", 27017).pmc.articles
    reporter = MongoQueryReporter(5, articles, query)
    finished = False
    while finished is False:
        finished = reporter.report()
        time.sleep(5)


with open("terms") as f:
    terms = [line.strip() for line in f.readlines()]

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo_host", default="localhost", dest="mongo_host")
    parser.add_argument("--mongo_port", default=27017)
    parser.add_argument("--keep_previous", action="store_true", dest="keep_previous")
    parser.add_argument("--num_workers", type=int, default=4, dest="num_workers")
    parser.add_argument("--silent", action="store_false", dest="report_progress")
    args = parser.parse_args()
    articles = pymongo.MongoClient(args.mongo_host, args.mongo_port).pmc.articles

    if not args.keep_previous:
        print("Dropping previously-matched terms...")
        articles.update_many(
            filter={},
            update={
                "$unset": {
                    "article_meta.n_geospans": "",
                    "article_meta.n_nonparen_geospans": "",
                    "article_meta.n_paren_geospans": "",
                    "article_meta.geospan_density": "",
                    "article_meta.nonparen_geospan_density": "",
                    "article_meta.paren_geospan_density": "",
                }
            },
        )

    query = {
        "text_matches": {"$in": terms},
        "$or": [
            {"article_meta.n_geospans": {"$exists": False}},
            {"article_meta.n_nonparen_geospans": {"$exists": False}},
            {"article_meta.n_paren_geospans": {"$exists": False}},
            {"article_meta.geospan_density": {"$exists": False}},
            {"article_meta.nonparen_geospan_density": {"$exists": False}},
            {"article_meta.paren_geospan_density": {"$exists": False}},
        ],
    }

    count = articles.count_documents(query)
    print("Updating GeoName count and density in {} documents...".format(count))

    cursor = articles.find(query, ["_id"])

    queue = mp.Queue()
    for x in cursor:
        queue.put(x)
    for x in range(args.num_workers):
        queue.put("STOP")

    workers = [
        mp.Process(target=do_work, args=(queue,)) for w in range(args.num_workers)
    ]

    for w in workers:
        w.start()

    interval = 5
    reporter = MongoQueryReporter(interval, articles, query)
    while count > 0:
        count = reporter.report()
        time.sleep(interval)

    for w in workers:
        w.join()

    print("Creating index on results...")
    articles.create_index("article_meta")

    print("Finished.")
