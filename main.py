from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig,DataValidationConfig,DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys

if __name__ == '__main__':
    try:
    
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info("initiate the data_ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info("data initiation completed")
        print(dataingestionartifact)
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(
        data_ingestion_artifact=dataingestionartifact,
        data_validation_config=data_validation_config,
        )

        logging.info("initiate the data_validation")
        data_validation_artifact=data_validation.initiate_data_validation()
        logging.info("data validation completed ")
        print(data_validation_artifact)
        logging.info("data transformation started ")
        data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)


    except Exception as e:
        raise NetworkSecurityException(e, sys)
