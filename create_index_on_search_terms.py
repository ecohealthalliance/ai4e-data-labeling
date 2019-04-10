#!/usr/bin/env python
import os
import pymongo
from collections import defaultdict

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mongo_host", default="localhost", dest="mongo_host"
    )
    parser.add_argument(
        "--mongo_port", default=27017
    )
    parser.add_argument(
        "--drop_matches", action="store_true", dest="drop_matches"
    )
    args = parser.parse_args()
    articles = pymongo.MongoClient(args.mongo_host, args.mongo_port).pmc.articles
    
    with open("terms") as f:
        terms = [line.strip() for line in f.readlines()]

    print("Creating text index...")

    # Make sure we have a text index
    articles.create_index([("extracted_text", pymongo.TEXT,)])

    if args.drop_matches:
        print("Dropping previously-matched terms...")
        articles.update_many(
            filter={},
            update={ "$unset": { "text_matches": "" } }
        )

    print("Searching for terms:")

    # Create a subdocument on the results of searches for terms.
    for term in terms:
        print(term)
        results = articles.update_many(
            filter={ '$text': { '$search': '"' + term + '"' } },
            update={ "$addToSet": { "text_matches": term} }
        )

    print("Creating index on search results...")
    articles.create_index("text_matches")

    print("Getting results...")

    by_term = dict()
    by_id = defaultdict(list)
    for term in terms:
        results = articles.find(
            { "text_matches": term },
            { '_id': '_id'}
        )
        result_set = {result["_id"] for result in results}
        by_term[term] = result_set
        [by_id[result].append(term) for result in result_set]

    print("Matches per term:")
    summary = [(term, len(ids)) for term, ids in by_term.items()]
    print(summary)
    print("Documents matching any term:")
    all_matches = set.union(*by_term.values())
    print(len(all_matches))