import sys
from json import loads
from typing import Collection
from pandas import DataFrame
from pymongo.database import Database
import pandas as pd
from pymongo import MongoClient
from shipment.constants import DB_URL
from shipment.exception import shippingException
from shipment.logger import logging 

class MongoDBOperation:
    def __init__(self):
        self.DB_URL = DB_URL
        self.client = MongoClient(self.DB_URL)

    def get_database(self , db_name:str)->Database:
        logging.info(f"Getting the database {db_name}")
        try:
            return self.client[db_name]
        except Exception as e:
            raise shippingException(e , sys) from e
        
    @staticmethod
    def get_collection( database , collection_name)->Collection:
        logging.info(f"Getting the get_collection of MongoDBOperation class")
        try:
            collection = database[collection_name]
            logging.info('Excited get_collection from MongoDB_Operation class')
            return collection
        
        except Exception as e:
            raise shippingException(e , sys) from e
        

    
    def get_collection_as_dataframe(self , db_name , collection_name)-> DataFrame:
        logging.info('Entered get_collection_as_dataframe of MongoDB_Operation class')

        try:
            database = self.get_database(db_name)
            collection = database.get_collection(collection_name)

            df = pd.DataFrame(list(collection.find()))
            if"_id" in df.columns.to_list():
                df = df.drop(columns = ["_id"] , axis = 1)
            
            logging.info(f"Converted collection to dataframe")
            return df
        except Exception as e:
            raise shippingException(e , sys) from e

        
    def insert_dataframe_as_record(self , data_frame , db_name , collection_name)-> None:
        logging.info(f"Inserting the dataframe as record in collection {collection_name}")
        try:
            records = loads(data_frame.T.to_json()).values()
            database = self.get_database(db_name)
            collection = database.get_collection(collection_name)
            collection.insert_many(records)
        except Exception as e:
            raise shippingException(e , sys) from e