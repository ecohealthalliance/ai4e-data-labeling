#!/usr/bin/env python
import os
import pymongo
from pubcrawler.article import Article
from random import sample, seed
from reporter import Reporter


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--pmc_path", default="pmc", dest="pmc_path"
    )
    parser.add_argument(
        "-n", default=1000, dest="n", type=int
    )
    parser.add_argument(
        "--mongo_host", default="localhost", dest="mongo_host"
    )
    parser.add_argument(
        "--mongo_port", default=27017
    )
    parser.add_argument(
        "-s", "--seed", default=None, dest="seed"
    )
    args = parser.parse_args()

    articles = pymongo.MongoClient(args.mongo_host, args.mongo_port).pmc.articles
    articles.drop()

    print("Gathering list of PMC files to sample...")

    all_files = []
    for (dirpath, dirnames, filenames) in os.walk(args.pmc_path):
        all_files += [os.path.join(dirpath, filename) for filename in filenames if filename.endswith("xml")]

    seed(args.seed)
    files = sample(all_files, args.n)

    print("Loading {} files into collection...\n".format(args.n))

    articles.drop()
    reporter = Reporter(25, len(files))
    for idx, file in enumerate(files):
        reporter.report(idx)
        with open(file, "r") as f:
            xml = f.read()
            article = Article(xml)
            articles.insert_one({
                "_id": article.pub_ids().get("pmc"),  # Assuming they all have them
                "xml": xml,
                "extracted_text": article.extract_text()
            })

    print("Loaded {} articles into MongoDB collection.".format(articles.count_documents({})))
