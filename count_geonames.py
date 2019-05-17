import time
import os
import sys
import multiprocessing as mp
import pymongo
from pubcrawler.article import Article
from epitator.annodoc import AnnoDoc
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
            article = AnnoDoc(record["extracted_text"]).add_tier(geoname_annotator)
            geospans = article.tiers["geonames"]
            all_geospans = len(geospans)
            n_geospans = sum(
                [1 for span in geospans if span.metadata["geoname"].score > 0.13]
            )
            geospan_density = n_geospans / len(record["extracted_text"])
        articles.update_one(
            i,
            {
                "$set": {
                    "article_meta.all_geospans": all_geospans,
                    "article_meta.n_geospans": n_geospans,
                    "article_meta.geospan_density": geospan_density,
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

    query = {
        "text_matches": {"$in": terms},
        "$or": [
            {"article_meta.n_geospans": {"$exists": False}},
            {"article_meta.geospan_density": {"$exists": False}},
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
