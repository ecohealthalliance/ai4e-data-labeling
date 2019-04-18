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

    query = {
        "text_matches": {"$in": terms},
        "article_meta.article_type": "research-article",
        "article_meta.has_body": True,
        "article_meta.n_geospans": {"$exists": True}
    }

    cursor = articles.aggregate([
        {"$match": query},
        {"$project": {"n_geospans": "$article_meta.n_geospans"}}
    ])

    geospan_df = pd.DataFrame(cursor)
    q25 = geospan_df.n_geospans.quantile(q=0.25)

    subset_query = {
        "text_matches": {"$in": terms},
        "article_meta.article_type": "research-article",
        "article_meta.has_body": True,
        "article_meta.n_geospans": {"$gte": q25}
    }

    print("Dumping articles matching this query:\n{}"
          .format(json.dumps(subset_query, indent=4)))

    subprocess.run(["mongodump", "--gzip", "--archive=ai4e_articles.gzip",
                    "-d", "pmc", "-c", "articles", "-q", json.dumps(subset_query)])
