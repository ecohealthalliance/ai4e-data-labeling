import subprocess
import json
import pandas as pd
import numpy as np
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
        "article_meta.n_geospans": {"$exists": True},
        "article_meta.geospan_density": {"$exists": True},
    }

    cursor = articles.aggregate([
        {"$match": simple_query},
        {"$project": {
            "n_geospans": "$article_meta.n_geospans",
            "geospan_density": "$article_meta.geospan_density",
            "length": {"$strLenCP": "$extracted_text"}
        }}
    ])

    subset_df = pd.DataFrame(cursor)
    quantiles = subset_df.quantile(q=[0.01, 0.25, 0.95, 0.99])

    density = subset_df["geospan_density"]
    density = density[density!=0]
    log_density = np.log(density)
    threshold_density = np.exp(np.mean(log_density) - np.std(log_density))

    final_query = {
        "text_matches": {"$in": terms},
        "article_meta.article_type": "research-article",
        "article_meta.has_body": True,
        "article_meta.n_geospans": {"$gt": quantiles.n_geospans.iloc[0],
                                    "$lte": quantiles.n_geospans.iloc[3]},
        "article_meta.geospan_density": {"$gt": threshold_density},
        "$and": [
            {"$expr": {"$gt": [{"$strLenCP": "$extracted_text"}, quantiles.length.iloc[0]]}},
            {"$expr": {"$lte": [{"$strLenCP": "$extracted_text"}, quantiles.length.iloc[2]]}}
        ]
    }

    print("Dumping {} articles matching this query:\n\n{}".format(
        articles.count_documents(final_query),
        json.dumps(final_query, indent=4)
        ))

    subprocess.run(["mongodump", "--gzip", "--archive=ai4e_articles.gzip",
                    "-d", "pmc", "-c", "articles", "-q", json.dumps(final_query)])
