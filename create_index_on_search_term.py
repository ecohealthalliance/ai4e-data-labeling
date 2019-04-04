import os
import pymongo

db = pymongo.MongoClient(os.environ["MONGO_HOST"]).pmc
db.comm_use_subset.create_index([('content', pymongo.TEXT,)])

results = db.comm_use_subset.find(
   { '$text': { '$search': '"field study"' } },
   { 'score': { '$meta': "textScore" } }
).sort([('score', {'$meta': 'textScore'})])

print(list(results))