#!/usr/bin/env python
import pymongo
from reporter import MongoQueryReporter
from pubcrawler.article import Article

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo_host", default="localhost", dest="mongo_host")
    parser.add_argument("--mongo_port", default=27017)
    parser.add_argument("--drop_previous", action="store_false", dest="keep_previous")
    args = parser.parse_args()
    articles = pymongo.MongoClient(args.mongo_host, args.mongo_port).pmc.articles

    if not args.keep_previous:
        print("Dropping previously-extracted metadata...")
        articles.update_many(
            filter={},
            update={
                "$unset": {
                    "article_title": "",
                    "journal_title": "",
                    "article_meta.has_body": "",
                    "article_meta.article_type": "",
                }
            },
        )

    query = {
        "$or": [
            {"article_title": {"$exists": False}},
            {"journal_title": {"$exists": False}},
            {"article_meta.has_body": {"$exists": False}},
            {"article_meta.article_type": {"$exists": False}},
        ]
    }

    count = articles.count_documents(query)

    print("Updating documents {} documents...".format(count))

    cursor = articles.find(query)
    reporter = MongoQueryReporter(1, articles, query)

    for idx, record in enumerate(cursor):
        article = Article(record["xml"])

        record_update = {
            "article_title": article.article_title(),
            "journal_title": article.journal_title(),
            "article_meta.has_body": True if article.soup.body else False,
            "article_meta.article_type": article.article_type(),
        }

        articles.update_one(
            filter={"_id": record["_id"]}, update={"$set": record_update}
        )

        reporter.report(idx)

    print("Creating index on results...")
    articles.create_index("article_meta")

    print("Testing index...")

    result_cursor = articles.aggregate(
        [
            {"$limit": 100},
            {"$group": {"_id": "$article_meta.article_type", "count": {"$sum": 1}}},
        ]
    )

    results = list(result_cursor)

    print("Breakdown of article types:")
    print(results)
