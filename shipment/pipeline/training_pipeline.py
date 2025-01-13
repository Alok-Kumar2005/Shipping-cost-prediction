import sys
from shipment.exception import shippingException
from shipment.logger import logging
from shipment.configuration.mongo_operation import MongoDBOperation
from shipment.entity.artifacts_entity import (
    DataIngestionArtifacts
)
from shipment.entity.config_entity import (
    DataIngestionConfig
)

from shipment.components.data_ingestion import DataIngestion

class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.mongo_op = MongoDBOperation()

    ## this method is used to start the data ingestion
    def start_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info('Enterd the start_data_ingestion method of TrainPipeline class')
        try:
            logging.info('Getting the data from mongodb')
            data_ingetsion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config , 
                mongo_op=self.mongo_op
            )

            data_ingetsion_artifacts = data_ingetsion.initiate_data_ingestion()
            logging.info('Got the train_set and test_set from mongodb')
            logging.info('Excited the start_data_ingestion method of TrainPipeline class')
            return data_ingetsion_artifacts
        except Exception as e:
            raise shippingException(e , sys)
        

    def run_pipeline(self)-> None:
        logging.info('Entered the run_pipeline method of TrainingPipeline class')
        try:
            data_ingestion_artifact = self.start_data_ingestion()

            logging.info("Excited the run_pipeline method of Training Pipline")

        except Exception as e:
            raise shippingException(e , sys) from e
