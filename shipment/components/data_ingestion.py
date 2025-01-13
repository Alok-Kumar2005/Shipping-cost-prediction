import sys
import os
import logging
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from typing import Tuple
from shipment.exception import shippingException
from shipment.configuration.mongo_operation import MongoDBOperation
from shipment.entity.config_entity import DataIngestionConfig
from shipment.entity.artifacts_entity import DataIngestionArtifacts
from shipment.constants import TEST_SIZE
from shipment.logger import logging as logger


class DataIngestion:
    def __init__(
            self, 
            data_ingestion_config: DataIngestionConfig, 
            mongo_op: MongoDBOperation):
        self.data_ingestion_config = data_ingestion_config
        self.mongo_op = mongo_op

    ## this method will featch dadta from mongodb
    def get_data_from_mongodb(self) -> DataFrame:
        logger.info("Enters get_data_from_mongodb method of data Ingestion class")
        try:
            logger.info("Getting the dataframe from mongodb")

            df = self.mongo_op.get_collection_as_dataframe(
                self.data_ingestion_config.DB_NAME,
                self.data_ingestion_config.COLLECTION_NAME,
            )

            logger.info('Got the dataframe from mongodb')
            logger.info('Exicited the get_data_from_mongodb method of dataIngestionMethod')

            return df
        except Exception as e:
            raise shippingException(e , sys) from e

    def split_data_as_train_test(self , df:DataFrame )-> Tuple[DataFrame , DataFrame]:
        logger.info('Enterd split_data_as_train_test method of Data_ingestion Class')
        try:
            os.makedirs(
                self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR , exist_ok= True
            )

            train_set , test_set = train_test_split(df , test_size = TEST_SIZE)
            logger.info("Performed train test split on the dataframe")

            ## creating train directory under data ingestion artifacts directory
            os.makedirs(
                self.data_ingestion_config.TRAIN_DATA_ARTIFACT_FILE_DIR , exist_ok= True
            )

            train_set.to_csv(
                self.data_ingestion_config.TRAIN_DATA_FILE_PATH,
                index = False,
                header = True,
            )

            test_set.to_csv(
                self.data_ingestion_config.TEST_DATA_FILE_PATH , Index = False , header = True
            )

            logger.info('Excited split_data_as_train_test method of DataIngestion class')

            return train_set , test_set
        
        except Exception as e:
            raise shippingException(e , sys) from e
        
    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        logger.info('Enterd initiate_data_ingestion method of DataIngestionClass')
        try:
            df = self.get_data_from_mongodb()

            ## Dropping the unnecessary column
            df1 = df.drop(self.data_ingestion_config.DROP_COLS , axis = 1)
            df1 = df1.dropna()

            logger.info('Got the data from the mongodb')
            self.split_data_as_train_test(df1)
            logger.info('Excited initiate_data_ingestion method of Data_Ingestion class')

            data_ingestion_artifacts = DataIngestionArtifacts(
                train_data_file_path=self.data_ingestion_config.TRAIN_DATA_FILE_PATH,
                test_data_file_path=self.data_ingestion_config.TEST_DATA_FILE_PATH
            )

            return data_ingestion_artifacts
        
        except Exception as e:
            raise shippingException(e , sys) from e