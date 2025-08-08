import os,sys
from src.exceptions import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass 
from src.modules.data_transform import DataTransformation
from src.modules.data_transform import DataTrasformationConfig

@dataclass #lets u use your class as a variable  itself
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'raw.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered into Data Ingestion Config: %s", self.ingestion_config)
        try:
            df=pd.read_csv('/home/alkanol/Desktop/__missIONs__/notebooks/data/stud.csv')
            logging.info("DataFrame Created")


            logging.info("Data Ingestion started")
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)  #os.path.dirname extracts directory name from the provided string
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info("Raw Data saved to %s", self.ingestion_config.raw_data_path)
            
            
            logging.info("Train Test Split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info("Train and Test Data saved")
             
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        
        except Exception as e:
            logging.error("Error occurred during Data Ingestion: %s", e)
            raise CustomException(e,sys)

if __name__ == "__main__":
    obj = DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    data_transformation.initiate_data_trans(train_data,test_data)