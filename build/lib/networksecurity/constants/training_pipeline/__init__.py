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

SCHEMA_FILE_NAME =os.path.join("data_schema","schema.yaml")

DATA_INGESTION_DATABASE_NAME: str = "network_security_db"
DATA_INGESTION_COLLECTION_NAME: str = "network_security_collection"
DATA_INGESTION_DIR_NAME: str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str="feature_store"
DATA_INGESTION_INGESTED_DIR: str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float=0.2

DATA_VALIDATION_VALID_DIR: str="validated"
DATA_VALIDATION_DIR_NAME: str="data_validation"
DATA_VALIDATION_INVALID_DIR: str="INVALID"
DATA_VALIDATION_DRIFT_REPORT_DIR: str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str="report.yaml"
