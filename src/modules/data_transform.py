# Feature
# Data Cleaning 
# Data Transforming

import os,sys
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer #creating pipelines
from sklearn.impute import SimpleImputer #missing_vals
from sklearn.pipeline import Pipeline  
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from src.exceptions import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import save_object

@dataclass
class DataTrasformationConfig:
    preprocessor_obj_path = os.path.join('artifacts',"preprocessor.pkl")
class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTrasformationConfig()
    def get_data_transformer(self):
        try:
            num_columns = ["writing_score","reading_score"]   
            cat_columns = [
            "gender",
            "race_ethnicity",
            "lunch",
            "parental_level_of_education",
            "test_preparation_course",
            ]     

            num_pipeline = Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scaler",StandardScaler())
                ]
            )
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("OHE",OneHotEncoder()),
                    ("scaler",StandardScaler(with_mean=False))
                ]
            )
            logging.info("Encoding and Standardisation Done....")

            preprocessor=ColumnTransformer(
                [
                    ("num_pipeline",num_pipeline,num_columns),
                    ("cat_pipeline",cat_pipeline,cat_columns),
                ]
            ) 
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_trans(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Completed ReReading of Train 'n' Test Data...")
    
            preprocessing_obj=self.get_data_transformer()
            tar_col_name  = "math_score"
            num_columns = ["writing_score","reading_score"]
    
            input_feat_train = train_df.drop(columns=[tar_col_name],axis =1)
            target_feat_train = train_df[tar_col_name]
    
            input_feat_test = test_df.drop(columns=[tar_col_name],axis =1)
            target_feat_test = test_df[tar_col_name]
            
            logging.info("Now Applying the Preprocessor om Data")
            
            input_feat_train_arr = preprocessing_obj.fit_transform(input_feat_train)
            input_feat_test_arr = preprocessing_obj.transform(input_feat_test)
            
            train_arr =  np.c_[
                input_feat_train_arr,np.array(target_feat_train)
            ]
            test_arr = np.c_[
                input_feat_test_arr,np.array(target_feat_test)
            ]
    
            logging.info("Saving Preprocessed Objects")
            
            save_object(
                file_path = self.data_transformation_config.preprocessor_obj_path,
                obj = preprocessing_obj
            )
    
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_path
            )
        except Exception as e:
            raise CustomException(e, sys)