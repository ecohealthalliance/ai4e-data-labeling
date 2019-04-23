import subprocess
import json
import pandas as pd
import pymongo
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mongo_host", default="localhost", dest="mongo_host"
    )
    parser.add_argument(
        "--mongo_port", default=27017
    )
    args = parser.parse_args()
    articles = pymongo.MongoClient(args.mongo_host,
                                   args.mongo_port).pmc.articles

    with open("terms") as f:
        terms = [line.strip() for line in f.readlines()]

    simple_query = {
        "text_matches": {"$in": terms},
        "article_meta.article_type": "research-article",
        "article_meta.has_body": True,
        "article_meta.n_geospans": {"$exists": True}
    }

    cursor = articles.aggregate([
        {"$match": simple_query},
        {"$project": {
            "n_geospans": "$article_meta.n_geospans",
            "length": {"$strLenCP": "$extracted_text"}
        }}
    ])

    subset_df = pd.DataFrame(cursor)
    quantiles = subset_df.quantile(q=[0.01, 0.25, 0.95, 0.99])

    final_query = {
        "text_matches": {"$in": terms},
        "article_meta.article_type": "research-article",
        "article_meta.has_body": True,
        "article_meta.n_geospans": {"$gt": quantiles.n_geospans.iloc[1],
                                    "$lt": quantiles.n_geospans.iloc[3]},
        "$expr": {"$gte": [{"$strLenCP": "$extracted_text"}, quantiles.length.iloc[0]]},
        "$expr": {"$lte": [{"$strLenCP": "$extracted_text"}, quantiles.length.iloc[2]]}
    }

    print("Dumping articles matching this query:\n{}"
          .format(json.dumps(final_query, indent=4)))

    subprocess.run(["mongodump", "--gzip", "--archive=ai4e_articles.gzip",
                    "-d", "pmc", "-c", "articles", "-q", json.dumps(final_query)])
