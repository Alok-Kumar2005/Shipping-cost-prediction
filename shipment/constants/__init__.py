import os
from os import environ
from datetime import datetime
from from_root.root import from_root


DB_URL = environ.get("MONGO_DB_URL")

MODEL_CONFIG_FILE = "config/model.yaml"

TIME_STAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
CONFIG_FILE_PATH = "config/config.yaml"
SCHEMA_FILE_PATH = "config/schema.yaml"

TARGET_COLUMN = 'Cost'
DB_NAME = 'shipmentdata'
COLLECTION_NAME = 'ship'
TEST_SIZE = 0.2
ARTIFACTS_DIR = os.path.join(from_root(), "artifacts" , TIME_STAMP)

DATA_INGESTION_ARTIFACTS_DIR = 'DataIngestionArtifacts'
DATA_INGESTION_TRAIN_DIR = "Train"
DATA_INGESTION_TEST_DIR = "Test"
DATA_INGESTION_TRAIN_FILE_NAME = "train.csv"
DATA_INGESTION_TEST_FILE_NAME = "test.csv"