#!/usr/bin/env python
import pymongo
from pubcrawler.article import Article
import os
import pandas as pd

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--mongo_host", default="localhost", dest="mongo_host")
    parser.add_argument("--mongo_port", default=27017)
    args = parser.parse_args()
    articles = pymongo.MongoClient(args.mongo_host, args.mongo_port).pmc.articles

    with open("terms") as f:
        terms = [line.strip() for line in f.readlines()]

    query = {
        "text_matches": {"$in": terms},
        "article_meta.article_type": "research-article",
        "article_meta.has_body": True,
        "article_meta.n_geospans": {"$exists": True},
    }

    cursor = articles.aggregate(
        [
            {"$match": query},
            {
                "$project": {
                    "n_geospans": "$article_meta.n_geospans",
                    "length": {"$strLenCP": "$extracted_text"},
                }
            },
        ]
    )

    subset_df = pd.DataFrame(cursor)
    subset_df.to_csv(os.path.join("data", "subset.csv"))
