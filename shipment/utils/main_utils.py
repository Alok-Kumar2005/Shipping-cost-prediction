import shutil
import sys
from typing import Dict , Tuple , List
import dill
import xgboost
import numpy as np
import pandas as pd
import yaml
from pandas import DataFrame
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.utils import all_estimators
from yaml import safe_dump
from shipment.constants import *
from shipment.exception import shippingException
from shipment.logger import logging as logger

class MainUtils:
    def read_yaml_file(self , filename:str) -> Dict:
        """
        Read the yaml file and return the dictionary
        """
        logger.info(f"Reading the yaml file {filename}")
        try:
            with open(filename , 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            raise shippingException(e , sys) from e
        
    def write_json_to_yaml(self , json_file:dict , yaml_file_path:str)-> yaml:
        logger.info('Entered the erite json to yaml file method of mainUtils class')
        try:
            data = json_file
            stream = open(yaml_file_path , 'w')
            yaml.dump(data , stream)
        except Exception as e:
            raise shippingException(e , sys) from e
        
    def save_numpy_array_data(self , file_path:str , array:np.array)->None:
        logger.info('Entered the save numpy array data method of mainUtils class')
        try:
            with open(file_path , 'wb') as file:
                np.save(file , array)
                return file_path
        except Exception as e:
            raise shippingException(e , sys) from e
        

    def load_numpy_array_data(self , file_path:str)->np.array:
        logger.info('Entered the load numpy array data method of mainUtils class')
        try:
            with open(file_path , 'rb') as file:
                return np.load(file)
        except Exception as e:
            raise shippingException(e , sys) from e
        
    def get_tuned_models(
            self,
            model_name:str,
            train_x:DataFrame,
            train_y:DataFrame,
            test_x:DataFrame,
            test_y:DataFrame,
    )-> Tuple[float , object , str]:
        logger.info("Entered the get_tuned_models method of mainUtils class")
        try:
            model = self.get_base_model(model_name)
            model_best_params = self.get_best_params(model , train_x , train_y)
            model.set_params(**model_best_params)
            model.fit(train_x , train_y)
            preds = model.predict(test_x)
            model_score = self.get_model_score(test_y , preds)
            logger.info("Excited the get_tuned_models method of mainUtils class")
            return model_score , model , model.__class__.__name__
        except Exception as e:
            raise shippingException(e , sys) from e
        
    @staticmethod
    def get_model_score(test_y:DataFrame , preds:DataFrame)->float:
        logger.info("Entered the get_model_score method of mainUtils class")
        try:
            return r2_score(test_y , preds)
        except Exception as e:
            raise shippingException(e , sys) from e
        
    @staticmethod
    def get_base_model(model_name:str)->object:
        logger.info("Entered the get_base_model method of mainUtils class")
        try:
            if model_name.lower().startswith("xgb") is True:
                model = xgboost.__dict__[model_name]()
            else:
                model_idx = [model[0] for model in all_estimators()].index(model_name)
                model = all_estimators()[model_idx][1]()
            logger.info("Excited the get_base_model method of mainUtils class")
            return model
                
        except Exception as e:
            raise shippingException(e , sys) from e
        

        #### 1:31