#!/usr/bin/env python
import os
import pymongo

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--pmc_path', default='pmc'
    )
    args = parser.parse_args()

    articles = pymongo.MongoClient(os.environ["MONGO_HOST"]).pmc.articles
    articles.drop()

    for (dirpath, dirnames, filenames) in os.walk(args.pmc_path):
        for name in filenames:
            filepath = os.path.join(dirpath, name)
            print(filepath)
            if filepath.endswith('txt'):
                base = os.path.basename(filepath)
                name = os.path.splitext(base)[0]
                with open(filepath, 'rb') as f:
                    article = {
                        '_id': name,
                        'path': filepath,
                        'content': f.read().decode('latin-1')                  }
                    articles.insert(article)
    print(articles.count())
