import sys 
import os 
import numpy as np
import pandas as pd 
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline 

from networksecurity.constants.training_pipeline import TARGET_COLUMN 
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import(
    DataTransformationArtifact,
    DataValidationArtifact

)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException 
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object
from networksecurity.utils.main_utils.utils import read_yaml_file
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH


class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
            self.data_transformation_config:DataTransformationConfig=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def get_data_transformer_object(cls)->Pipeline:
        
        logging.info(
            "Entered get_data_trnasformer_object method of Trnasformation class"
        )
        try:
           imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
           logging.info(
                f"Initialise KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}"
            )
           processor:Pipeline=Pipeline([("imputer",imputer)])
           return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation")
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df  = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            logging.info(f"Train columns: {list(train_df.columns)}")
            logging.info(f"Test columns: {list(test_df.columns)}")

            # --- Resolve target column dynamically using schema or fallbacks ---
            schema = read_yaml_file(SCHEMA_FILE_PATH)
            preferred = schema.get("target_column", "CLASS_LABEL")
            candidates = [preferred, "CLASS_LABEL", "label", "Result"]

            def _resolve(df):
                for c in candidates:
                    if c in df.columns:
                        return c
                raise Exception(
                    f"Target column not found. Looked for {candidates}. "
                    f"CSV columns: {list(df.columns)}"
                )

            target_col_train = _resolve(train_df)
            target_col_test  = _resolve(test_df)

            # --- Drop duplicate label columns (keep only the resolved target) ---
            dup_labels = [c for c in ["CLASS_LABEL", "label", "Result"] if c != target_col_train]
            train_df = train_df.copy()
            test_df  = test_df.copy()
            train_df.drop(columns=[c for c in dup_labels if c in train_df.columns], inplace=True, errors="ignore")
            test_df.drop(columns=[c for c in dup_labels if c in test_df.columns], inplace=True, errors="ignore")

            # --- Split features and targets using resolved column ---
            input_feature_train_df = train_df.drop(columns=[target_col_train], axis=1)
            target_feature_train_df = train_df[target_col_train].replace(-1, 0)

            input_feature_test_df = test_df.drop(columns=[target_col_test], axis=1)
            target_feature_test_df = test_df[target_col_test].replace(-1, 0)

            # --- Build and fit preprocessing pipeline ---
            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature  = preprocessor_object.transform(input_feature_test_df)

            # --- Combine transformed data with targets ---
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr  = np.c_[transformed_input_test_feature,  np.array(target_feature_test_df)]

            # --- Save arrays and preprocessor objects ---
            save_numpy_array_data(
                self.data_transformation_config.transformed_train_file_path,
                array=train_arr,
            )
            save_numpy_array_data(
                self.data_transformation_config.transformed_test_file_path,
                array=test_arr,
            )
            save_object(
                self.data_transformation_config.transformed_object_file_path,
                preprocessor_object,
            )
            save_object("final_model/preprocessor.pkl", preprocessor_object)

            # --- Create and return artifact ---
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
