from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_NAME
import os,sys 
import pandas as pd 
from scipy.stats import ks_2samp, chi2_contingency  
from pandas.api.types import is_numeric_dtype       


from networksecurity.utils.main_utils import read_yaml_file,write_yaml_file
class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.schema_file_path = SCHEMA_FILE_NAME
            self._schema_config = read_yaml_file(self.schema_file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)


        
    @staticmethod 
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            cols_cfg = None
            if isinstance(self._schema_config, dict):
                cols_cfg = self._schema_config.get("columns")

            if isinstance(cols_cfg, dict):
                required_cols = list(cols_cfg.keys())
            elif isinstance(cols_cfg, list):
                required_cols = cols_cfg
            else:
                logging.warning("No 'columns' in schema; skipping strict column-count check.")  # CHANGED
                return True  

            number_of_columns = len(required_cols)  
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {len(dataframe.columns)}")
            return len(dataframe.columns)==number_of_columns

        except Exception as e :
            raise NetworkSecurityException(e,sys)
        

    def datect_dataset_drift(self, base_df, current_df, threshold=0.05) -> bool:
        try:
            status = True
            report = {}
            skip = {"id", "CLASS_LABEL"}  

            for column in base_df.columns:
                if column in skip:
                    continue

            # per-column comparison
                s1 = base_df[column].dropna()
                s2 = current_df[column].dropna()

                if len(s1) == 0 or len(s2) == 0:
                    p = 1.0
                    drift = False
                else:
                # numeric first (KS), else categorical (chi-square)
                    s1n = pd.to_numeric(s1, errors="coerce").dropna()
                    s2n = pd.to_numeric(s2, errors="coerce").dropna()
                    if len(s1n) > 0 and len(s2n) > 0:
                        p = float(ks_2samp(s1n, s2n).pvalue)
                        drift = p < threshold
                    else:
                        c1 = s1.astype(str).value_counts()
                        c2 = s2.astype(str).value_counts()
                        cats = sorted(set(c1.index).union(set(c2.index)))
                        obs = [[int(c1.get(k, 0)), int(c2.get(k, 0))] for k in cats]
                        _, p, _, _ = chi2_contingency(obs, correction=False)
                        p = float(p)
                        drift = p < threshold

                if drift:
                    status = False

                report[column] = {"p_value": p, "drift_status": drift}

        # write once & return
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)
            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)


           

    
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path  = self.data_ingestion_artifact.test_file_path


            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)
            error_message=""
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message+="train datafrrame does not contain all the columns\n"
            status=self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message+="test datafrrame does not contain all the columns\n"
            
            status=self.datect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            )
            data_validation_artifact = DataValidationArtifact(
            validation_status=status,
            valid_train_file_path=self.data_validation_config.valid_train_file_path,
            valid_test_file_path=self.data_validation_config.valid_test_file_path,
            invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
            invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
            drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

            
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e,sys)