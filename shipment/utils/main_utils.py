import shutil
import sys
from typing import Dict, Tuple, List
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
    def read_yaml_file(self, filename: str) -> Dict:
        """
        Reads a YAML file and returns its content as a dictionary.
        """
        logger.info(f"Reading the YAML file {filename}")
        try:
            with open(filename, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            raise shippingException(e, sys) from e

    def write_json_to_yaml(self, json_file: dict, yaml_file_path: str) -> None:
        """
        Writes a JSON object to a YAML file.
        """
        logger.info('Entered the write_json_to_yaml method of MainUtils class')
        try:
            with open(yaml_file_path, 'w') as stream:
                yaml.dump(json_file, stream)
        except Exception as e:
            raise shippingException(e, sys) from e

    def save_numpy_array_data(self, file_path: str, array: np.ndarray) -> str:
        """
        Saves a NumPy array to a file.
        """
        logger.info('Entered the save_numpy_array_data method of MainUtils class')
        try:
            with open(file_path, 'wb') as file:
                np.save(file, array)
            return file_path
        except Exception as e:
            raise shippingException(e, sys) from e

    def load_numpy_array_data(self, file_path: str) -> np.ndarray:
        """
        Loads a NumPy array from a file.
        """
        logger.info('Entered the load_numpy_array_data method of MainUtils class')
        try:
            with open(file_path, 'rb') as file:
                return np.load(file)
        except Exception as e:
            raise shippingException(e, sys) from e

    def get_tuned_models(
            self,
            model_name: str,
            train_x: DataFrame,
            train_y: DataFrame,
            test_x: DataFrame,
            test_y: DataFrame,
    ) -> Tuple[float, object, str]:
        """
        Tunes a model, fits it to training data, and evaluates its performance.
        """
        logger.info("Entered the get_tuned_models method of MainUtils class")
        try:
            model = self.get_base_model(model_name)
            best_params = self.get_best_params(model, train_x, train_y)
            model.set_params(**best_params)
            model.fit(train_x, train_y)
            preds = model.predict(test_x)
            model_score = self.get_model_score(test_y, preds)
            logger.info("Exited the get_tuned_models method of MainUtils class")
            return model_score, model, model.__class__.__name__
        except Exception as e:
            raise shippingException(e, sys) from e

    @staticmethod
    def get_model_score(test_y: DataFrame, preds: np.ndarray) -> float:
        """
        Computes the R^2 score for the model's predictions.
        """
        logger.info("Entered the get_model_score method of MainUtils class")
        try:
            return r2_score(test_y, preds)
        except Exception as e:
            raise shippingException(e, sys) from e

    @staticmethod
    def get_base_model(model_name: str) -> object:
        """
        Fetches the base model object based on its name.
        """
        logger.info("Entered the get_base_model method of MainUtils class")
        try:
            if model_name.lower().startswith("xgb"):
                model = xgboost.__dict__[model_name]()
            else:
                available_models = {name: estimator for name, estimator in all_estimators()}
                if model_name not in available_models:
                    raise ValueError(f"Model {model_name} not found in available estimators.")
                model = available_models[model_name]()
            logger.info("Exited the get_base_model method of MainUtils class")
            return model
        except Exception as e:
            raise shippingException(e, sys) from e

    def get_best_params(self, model, train_x: DataFrame, train_y: DataFrame) -> Dict:
        """
        Finds the best hyperparameters for a model using GridSearchCV.
        (You need to define or modify this method as per your grid search requirements.)
        """
        logger.info("Entered the get_best_params method of MainUtils class")
        try:
            # Define a default parameter grid or customize as needed.
            param_grid = {}  # Add appropriate parameters for the model
            grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5)
            grid_search.fit(train_x, train_y)
            return grid_search.best_params_
        except Exception as e:
            raise shippingException(e, sys) from e

        

        #### 1:31