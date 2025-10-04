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
import certifi
from dotenv import load_dotenv
load_dotenv(".env")  # this loads the .env in your project root



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
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
            collection = self.mongo_client[database_name][collection_name]

            # Read all documents, drop _id at the query level
            cursor = collection.find({}, {"_id": 0})
            df = pd.DataFrame(list(cursor))

            # Hard checks to avoid empty splits
            if df.empty:
                raise ValueError(f"No documents found in '{database_name}.{collection_name}'")

            # Standardize and clean
            df.replace({"na": np.nan, "NA": np.nan, "": np.nan}, inplace=True)

            # Drop columns that are entirely NaN (but only if it doesn't nuke everything)
            all_nan_cols = df.columns[df.isna().all()]
            if len(all_nan_cols) > 0 and len(all_nan_cols) < len(df.columns):
                df = df.drop(columns=list(all_nan_cols), axis=1)

            if df.shape[1] == 0:
                raise ValueError("All columns are NaN after cleaning. Check source data/schema.")

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_feature_store(self,dataframe:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(
    train_file_path=self.data_ingestion_config.training_file_path,
    test_file_path=self.data_ingestion_config.testing_file_path,
    feature_store_file_path=self.data_ingestion_config.feature_store_file_path
)


            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
 
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            n = len(dataframe)
            if n < 2:
                raise ValueError(f"Not enough samples to split. Found n={n}. Load more data.")

            test_ratio = self.data_ingestion_config.train_test_split_ratio
            if not (0.0 < test_ratio < 1.0):
                raise ValueError(f"Invalid test_size: {test_ratio}")

            train_set, test_set = train_test_split(
                dataframe, test_size=test_ratio, random_state=42, shuffle=True
            )
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited the split_data_as_train_test method of Data Ingestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting training dataset to file path : {self.data_ingestion_config.training_file_path}")
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)

            logging.info(f"Exporting testing dataset to file path : {self.data_ingestion_config.testing_file_path}")
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
