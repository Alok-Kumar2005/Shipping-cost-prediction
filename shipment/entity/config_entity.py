from dataclasses import dataclass
from from_root.root import from_root
import os
# from shipment.configuration.s3_operations import S3Operations
from shipment.utils.main_utils import MainUtils
from shipment.constants import *

@ dataclass
class DataIngestionConfig:
    def __init__(self):
        self.UTILS = MainUtils()
        self.SCHEMA_CONFIG = self.UTILS.read_yaml_file(from_root(SCHEMA_FILE_PATH))
        self.DB_NAME = DB_NAME
        self.COLLECTION_NAME = COLLECTION_NAME
        self.DROP_COLS = list(self.SCHEMA_CONFIG["drop_cols"])
        self.DATA_INGESTION_ARTIFACTS_DIR: str = os.path.join(
            from_root() , ARTIFACTS_DIR , DATA_INGESTION_ARTIFACTS_DIR
        )
        self.TRAIN_DATA_ARTIFACTS_FILE_DIR: str = os.path.join(
            self.DATA_INGESTION_ARTIFACTS_DIR , DATA_INGESTION_TRAIN_DIR
        )
        self.TEST_DATA_ARTIFACTS_FILE_DIR: str = os.path.join(
            self.DATA_INGESTION_ARTIFACTS_DIR , DATA_INGESTION_TEST_DIR
        )
        self.TRAIN_DATA_FILE_PATH: str = os.path.join(
            self.TRAIN_DATA_ARTIFACTS_FILE_DIR , DATA_INGESTION_TRAIN_FILE_NAME
        )
        self.TEST_DATA_FILE_PATH: str = os.path.join(
            self.TEST_DATA_ARTIFACTS_FILE_DIR , DATA_INGESTION_TEST_FILE_NAME
        )