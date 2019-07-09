#!/usr/bin/env python
import pymongo
from reporter import MongoQueryReporter
from pubcrawler.article import Article

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo_host", default="localhost", dest="mongo_host")
    parser.add_argument("--mongo_port", default=27017)
    args = parser.parse_args()
    articles = pymongo.MongoClient(args.mongo_host, args.mongo_port).pmc.articles

    query = {}

    count = articles.count_documents(query)

    print("Updating documents {} documents...".format(count))

    cursor = articles.find({})
    reporter = MongoQueryReporter(1, articles, {})

    for idx, record in enumerate(cursor):
        article = Article(record["xml"])

        record_update = {
            "extracted_text": article.extract_text()
        }

        articles.update_one(
            filter={"_id": record["_id"]}, update={"$set": record_update}
        )

        reporter.report(idx)

    print("Reprocessed article text.")
