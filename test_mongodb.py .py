from pymongo.mongo_client import MongoClient
from urllib.parse import quote_plus
from urllib.parse import quote_plus
username = "sairathan201820_db_user"
password = quote_plus("Tenneti@131223")

uri = "mongodb+srv://sairathan201820_db_user:Tenneti%40131223@cluster0.lpnq2x7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)