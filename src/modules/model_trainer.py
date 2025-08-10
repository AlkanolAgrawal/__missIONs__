import os,sys

from matplotlib.pylab import sort
from src.exceptions import CustomException
from src.logger import logging
from src.utils import evaluate_models, save_object
from dataclasses import dataclass

from catboost import CatBoostRegressor
import sklearn
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

@dataclass
class ModelTrainerConfig:
    trained_model_path:str = os.path.join("artifacts","trained_model.pkl")  

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self,train_array,test_array):
        try:
            logging.info("Splitting train and test data")
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1],
                train_array[:,-1],
                test_array[:,:-1],
                test_array[:,-1]
            )
            models = {
                "LinearRegression": LinearRegression(),
                "KNeighborsRegressor": KNeighborsRegressor(),
                "DecisionTreeRegressor": DecisionTreeRegressor(),
                "RandomForestRegressor": RandomForestRegressor(),
                "GradientBoostingRegressor": GradientBoostingRegressor(),
                "AdaBoostRegressor": AdaBoostRegressor(),
                "XGBRegressor": XGBRegressor(verbosity=0),
                "CatBoostRegressor": CatBoostRegressor(verbose=0)
            }

            parameters = {
                "LinearRegression": {},
                "KNeighborsRegressor": {
                    "n_neighbors": [3, 5, 7],
                    "weights": ["uniform", "distance"],
                    "algorithm": ["ball_tree", "kd_tree"]
                },
                "DecisionTreeRegressor": {
                    'criterion': ['squared_error', 'absolute_error', 'poisson'],
                    # 'splitter': ['best', 'random'],
                    'max_features': ['auto', 'sqrt', 'log2'],
                    'max_depth': [10, 20, 30]
                },
                "RandomForestRegressor": {
                    'criterion': ['squared_error', 'absolute_error', 'poisson'],
                    'max_features': ['auto', 'sqrt', 'log2'],
                    'max_depth': [10, 20, 30],
                    'n_estimators': [10,50,100]
                },
                "GradientBoostingRegressor": {
                    'loss': ['squared_error', 'huber', 'quantile'],
                    'learning_rate': [0.01, 0.1, 0.2],
                    'n_estimators': [10, 50, 100],
                    'max_depth': [10, 20, 30],
                    # 'max_features': ['auto', 'sqrt', 'log2']
                },
                "AdaBoostRegressor": {
                    'n_estimators': [10, 50, 100],
                    'learning_rate': [0.01, 0.1]
                },
                "XGBRegressor": {
                    'n_estimators': [10, 50, 100],
                    'max_depth': [10, 20, 30],
                    'learning_rate': [0.01, 0.1, 0.2]
                },
                "CatBoostRegressor": {
                    'iterations': [100, 200, 300],
                    'depth': [10, 20, 30],
                    'learning_rate': [0.01, 0.1, 0.2]
                }
            }

            model_report :dict = evaluate_models(X_train,y_train,X_test,y_test,models,parameters)
            model_report = sorted(model_report.items(), key=lambda x: x[1], reverse=True)
            logging.info(f"Model report: {model_report}")
            print(f"Model report: {model_report}")

            best_model_name = model_report[0][0]
            best_model = models[best_model_name]
            logging.info(f"Best model: {best_model_name} with R2 score: {model_report[0][1]}")
            save_object(
                file_path=self.model_trainer_config.trained_model_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            return r2_score(y_test, predicted)
        except Exception as e:
            raise CustomException(e, sys)
        