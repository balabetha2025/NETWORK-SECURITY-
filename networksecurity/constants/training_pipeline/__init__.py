from datetime import datetime
import os
import sys
import pandas as pd 
import numpy as np

TARGET_COLUMN="Result"
PIPELINE_NAME:str="network_security_pipeline"
ARTIFACT_DIR:str="artifact"
FILE_NAME:str="Phishing_legitimate_full.csv"

TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"

DATA_INGESTION_COLLECTION_NAME: str="network_security_db.network_security_collection"
DATA_INGESTION_DATABASE_NAME: str="network_security_db"
DATA_INGESTION_DIR_NAME: str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str="feature_store"
DATA_INGESTION_INGESTED_DIR: str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float=0.2

