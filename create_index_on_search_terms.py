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
        "-t",
        "--terms",
        default=["field work",
                 "fieldwork",
                 "field study",
                 "study site"],
        nargs="+",
        dest="terms")

    args = parser.parse_args()
    terms = args.terms

    articles = pymongo.MongoClient(args.mongo_host, args.mongo_port).pmc.articles

    # Make sure we have a text index
    articles.create_index([("extracted_text", pymongo.TEXT,)])

    # Create a subdocument on the results of searches for terms.
    for term in terms:
        results = articles.update_many(
            filter={ '$text': { '$search': '"' + term + '"' } },
            update={ "$addToSet": { "text_matches": term} }
        )
    articles.create_index("text_matches")

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

    summary = [(term, len(ids)) for term, ids in by_term.items()]
    print(summary)