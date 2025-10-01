from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os 
import sys 
import numpy as np
import pandas as pd
import pymongo 
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def export_collection_as_dataframe(self):

        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            logging.info(f"Using DB: {database_name}")
            logging.info(f"Using Collection: {collection_name}")
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            collection=self.mongo_client[database_name][collection_name]
            print("DB =", database_name)
            print("COL =", collection_name)
            doc_count = collection.count_documents({})
            print("DOC_COUNT =", doc_count)

            df = pd.DataFrame(list(collection.find()))
            print("DF_SHAPE =", df.shape)
            print("DF_HEAD =", df.head(1).to_dict(orient="records"))
            
            



            
            if "_id" in df.columns:
                df = df.drop(columns=["_id"],axis=1)

            df.replace({"na": np.nan},inplace=True)
            return df 

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def export_data_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            self.export_data_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            dataingestionartifact = DataIngestionArtifact(
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
            train_file_path=self.data_ingestion_config.training_file_path,
            test_file_path=self.data_ingestion_config.testing_file_path
        )


            
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
 
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Performed train test split on the dataframe")

            logging.info("Exited the split_data_as_train_test method of Data Ingestion class" )

            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Exporting training dataset to file path : {self.data_ingestion_config.training_file_path}")

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info(f"Exporting testing dataset to file path : {self.data_ingestion_config.testing_file_path}")
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)