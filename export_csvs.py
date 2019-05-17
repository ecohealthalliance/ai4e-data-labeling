import os
import pymongo
from pubcrawler.article import Article
from reporter import Reporter
import pandas as pd
import numpy as np


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pmc_path", default="pmc", dest="pmc_path")
    parser.add_argument("-n", default=1000, dest="n", type=int)
    parser.add_argument("--mongo_host", default="localhost", dest="mongo_host")
    parser.add_argument("--mongo_port", default=27017)
    parser.add_argument("-s", "--seed", default=None, dest="seed")
    args = parser.parse_args()

    articles = pymongo.MongoClient(args.mongo_host, args.mongo_port).pmc.articles

    count = articles.count_documents({})
    cursor = articles.find({})
    reporter = Reporter(25, count)
    rows = []

    for idx, record in enumerate(cursor):
        row = {}
        article = Article(record["xml"])

        row["id"] = record["_id"]
        row["keywords"] = article.keywords()
        row["id_types"] = list(article.pub_ids().keys())
        row["article_type"] = article.article_type()
        row["has_body"] = True if article.soup.body else False
        row["text_matches"] = record.get("text_matches")
        row["article_title"] = article.article_title()
        row["journal_title"] = article.journal_title()
        row["text_length"] = len(record["extracted_text"])

        rows.append(row)
        reporter.report(idx)

    article_df = pd.DataFrame.from_records(rows)
    article_df["any_matches"] = [
        False if row is None else True for row in article_df["text_matches"]
    ]

    # Small function to unnest nested iterables.
    def unnest(data, unnest_var, keep_vars):
        nested = article_df.loc[:, keep_vars + [unnest_var]]
        lens = [len(item) if item is not None else 1 for item in nested[unnest_var]]
        unnested_dict = {
            var: np.repeat([nested[var].values], lens) for var in keep_vars
        }
        unnested_dict[unnest_var] = np.hstack(nested[unnest_var])
        unnested = pd.DataFrame(unnested_dict)
        return unnested

    keywords = unnest(article_df, "keywords", ["id", "any_matches"])
    id_types = unnest(article_df, "id_types", ["id", "any_matches"])
    text_matches = unnest(article_df, "text_matches", ["id"])

    article_df.to_csv(os.path.join("data", "articles.csv"))
    keywords.to_csv(os.path.join("data", "keywords.csv"))
    id_types.to_csv(os.path.join("data", "id_types.csv"))
    text_matches.to_csv(os.path.join("data", "text_matches.csv"))
