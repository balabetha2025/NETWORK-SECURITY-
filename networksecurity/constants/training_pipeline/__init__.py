from datetime import datetime
import os
import sys
import pandas as pd 
import numpy as np

TARGET_COLUMN="label"
PIPELINE_NAME:str="networksecurity"
ARTIFACT_DIR:str="Artifacts"
FILE_NAME:str="PhishingData.csv"

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
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"


DATA_TRANSFORMATION_DIR_NAME: str= "data_transofrmation"
DATA_TRANSFORMATION_TRANSFORMERD_DATA_DIR: str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECTT_DIR: str = "transformed_object"


DATA_TRANSOFRMATION_IMPUTER_PARAMS:dict = {
     "missing_values":np.nan,
     "n_neighbors": 3,
     "weights": "uniform",
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"

DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"



MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD: float = 0.05

TRAINING_BUCKET_NAME = "netwworksecurity"


