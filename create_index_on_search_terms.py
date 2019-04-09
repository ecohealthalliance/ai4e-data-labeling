#!/usr/bin/env python
import os
import pymongo

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



    results = db.comm_use_subset.find(
       { '$text': { '$search': '"field study"' } },
       { 'score': { '$meta': "textScore" } }
    ).sort([('score', {'$meta': 'textScore'})])

    print(list(results))