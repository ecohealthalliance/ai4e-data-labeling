#!/usr/bin/env python
import os
import pymongo
from pubcrawler.article import Article
from random import sample, seed
import time
from statistics import mean


class Reporter:
    def __init__(self, interval, total):
        self.start = time.time()
        self.this_time = self.start
        self.interval = interval
        self.total = total
        self.times_per_batch = []

    def report(self, idx):
        self.last_time = self.this_time
        self.this_time = time.time()
        time_per = (self.this_time - self.last_time) / self.interval
        self.times_per_batch.append(time_per)
        est_time_left = (self.total - idx) * mean(self.times_per_batch[-10:])
        elapsed = time.time() - self.start

        output = "\033[F\033[K" + "Processed {0} articles ({1:.1f}%) in {2:.0f}m{3:.0f}s; about {4:.0f}m{5:.0f}s left.".format(
            idx,
            idx/self.total * 100,
            elapsed // 60,
            elapsed % 60,
            est_time_left // 60,
            est_time_left % 60)
        print(output)


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
    reporter = Reporter(50, len(files))
    for idx, file in enumerate(files):
        if idx is not 0 and idx % reporter.interval is 0:
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
