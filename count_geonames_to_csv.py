#!/usr/bin/env python
import os
import pymongo

import pandas as pd

from epitator.annodoc import AnnoDoc
from epitator.geoname_annotator import GeonameAnnotator

from reporter import Reporter

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", default=250, dest="n", type=int
    )
    parser.add_argument(
        "--mongo_host", default="localhost", dest="mongo_host"
    )
    parser.add_argument(
        "--mongo_port", default=27017
    )
    args = parser.parse_args()
    articles = pymongo.MongoClient(args.mongo_host,
                                   args.mongo_port).pmc.articles
    n = args.n

    geoname_annotator = GeonameAnnotator()

    # Sample documents
    with open("terms") as f:
        terms = [line.strip() for line in f.readlines()]

    terms_cursor = articles.find({"text_matches": {"$in": terms}}, limit=n)
    noterms_cursor = articles.find({
        "text_matches": {"$not": {"$in": terms}}
    }, limit=n)
    sample = list(terms_cursor) + list(noterms_cursor)

    reporter = Reporter(5, len(sample))

    # Count GeoNames in sample and construct DataFrame
    rows = []
    for idx, record in enumerate(sample):
        row = {}
        article = AnnoDoc(record["extracted_text"]).add_tier(geoname_annotator)
        geospans = article.tiers["geonames"]
        row["text_matches"] = record.get("text_matches")
        row["n_spans"] = len(geospans)
        row["n_spans_over90"] = sum([1 for span in geospans
                                     if span.metadata["geoname"].score > 0.9])
        rows.append(row)
        reporter.report(idx)

    df = pd.DataFrame.from_records(rows)
    df["any_matches"] = [False if row is None else True
                         for row in df["text_matches"]]

    # Print summaries
    print(df.loc[df["any_matches"]].describe())
    print(df.loc[~df["any_matches"]].describe())

    df.to_csv(os.path.join("data", "geonames.csv"))
