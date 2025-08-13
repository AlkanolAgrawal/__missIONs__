import os , sys
from src.logger import logging
import pandas as pd
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exceptions import CustomException

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            dill.dump(obj, file)
    except Exception as e:
        raise CustomException(e, sys)

def evaluate_models(X_train, y_train, X_test, y_test, models, parameters):
    try:
        model_report = {}
        for model_name, model in models.items():
            logging.info(f"Training model: {model_name}")
            gs = GridSearchCV(
                estimator=model,
                param_grid=parameters[model_name],
                cv=5,
                n_jobs=-1,
                verbose=0
            )
            gs.fit(X_train, y_train)
            model.set_params(**gs.best_params_)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            model_report[model_name] = r2_score(y_test, y_pred)
        return model_report
    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path, 'rb') as file:
            return dill.load(file)
    except Exception as e:
        raise CustomException(e, sys)
    

def get_requireds(file_path):
    with open(file_path) as f:
        lst = f.readlines()
        lstn=[]
        for x in lst:
            a=x.strip()
            if a == "":
                continue
            if "-e ." == a:
                continue
            else:
                lstn.append(a)
    return lstn