import subprocess
import json

if __name__ == "__main__":
    with open("terms") as f:
        terms = [line.strip() for line in f.readlines()]

    query = {
        "text_matches": { 
            "$in": terms
        },
        "article_meta": {
            "has_body": True,
            "article_type": "research-article"
        }
    }

    subprocess.run(["mongodump", "--gzip", "--archive=ai4e_articles.gzip", "-d", "pmc", "-c", "articles", "-q", json.dumps(query)])
