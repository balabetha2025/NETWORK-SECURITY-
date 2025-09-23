from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig, trainingPipelineConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys

if __name__ == '__main__':
    try:
    
        trainingpipelineconfig = trainingPipelineConfig()

    
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)

    
        data_ingestion = DataIngestion(data_ingestion_config=dataingestionconfig)

        logging.info("initiate the data_ingestion")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifact)

    except Exception as e:
        raise NetworkSecurityException(e, sys)
