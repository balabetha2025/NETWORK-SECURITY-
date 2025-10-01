import os, pymongo, certifi
from dotenv import load_dotenv
load_dotenv()


MONGO_DB_URL = os.getenv("MONGO_DB_URL")


DB = "network_security_db"
COL = "network_security_collection"

client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
col = client[DB][COL]


docs = [
    {"feature1": 10, "feature2": 20, "label": 1},
    {"feature1": 30, "feature2": 40, "label": 0},
    {"feature1": 50, "feature2": 60, "label": 1},
]

col.insert_many(docs)
print("Now docs:", col.count_documents({}))
