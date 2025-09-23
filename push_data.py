import os 
import sys
import json 
import pymongo

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")


import certifi
ca=certifi.where()


import pandas as pd 
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging 

class NetworkSecurityData:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    def csv_to_json_converter(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records 
            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def insert_data_mongodb(self,records,database,collection):
        try:
            if isinstance(records,list):
                self.database=database 
                self.collection=collection
                self.records =records

                self.mongo_client=pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
                self.mongo_client.admin.command("ping")
                print("MongoDB connection successful ✅")
                self.database=self.mongo_client[self.database]
                
                self.collection=self.database[self.collection]
                self.collection.insert_many(self.records)
                return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
if __name__=='__main__':
    FILE_PATH="network_data/Phishing_Legitimate_full.csv"
    DATABASE="network_security_db"
    COLLECTION="network_security_collection"
    networkobj=NetworkSecurityData()
    records=networkobj.csv_to_json_converter(file_path=FILE_PATH)
    no_of_records=networkobj.insert_data_mongodb(records=records,database=DATABASE,collection=COLLECTION)
    print(no_of_records)