import sys
from src.exception import MyException
from src.logger import logging

from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
'''
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher
'''
from src.entity.config_entity import (DataIngestionConfig,
                                      DataValidationConfig,
                                      DataTransformationConfig,
                                      ModelTrainerConfig,)
                                          
from src.entity.artifact_entity import (DataIngestionArtifact,
                                         DataValidationArtifact,
                                         DataTransformationArtifact,
                                         ModelTrainerArtifact,)



class TrainPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()#data ingestion ki config class ka object bnaya
        self.data_validation_config = DataValidationConfig()#data validation ki config class ka object bnaya
        self.data_transformation_config = DataTransformationConfig()#data transformation ki config class ka object bnaya
        self.model_trainer_config = ModelTrainerConfig()#model trainer ki config class ka object bnaya
    
    def start_data_ingestion(self) -> DataIngestionArtifact:
        """
        This method of TrainPipeline class is responsible for starting data ingestion component
        """
        try:
            logging.info("Entered the start_data_ingestion method of TrainPipeline class")
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the train_set and test_set from mongodb")
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifact #returning the path of the artifacts ... which was configured in the config file(artifacts) 
        except Exception as e:
            raise MyException(e, sys) from e
        

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        """
        This method of Trainpipline check's that the data pulled from the dataBase and after conversion,
        have the required columns ( nums as well as catergorical ) present or not 
        """
        try:
            logging.info("Entered the start_data_validation method of TrainPipeline class")
            data_validation = DataValidation(data_validation_config=self.data_validation_config,
                                             data_ingestion_artifact=data_ingestion_artifact
                                             )
            
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Perforned the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")

            return data_validation_artifact
        except Exception as e:
            raise MyException(e, sys)
        


    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        """
        This method of TrainPipeline class is responsible for starting data transformation component
        """
        try:
            data_transformation = DataTransformation(data_ingestion_artifact=data_ingestion_artifact,
                                                     data_transformation_config=self.data_transformation_config,
                                                     data_validation_artifact=data_validation_artifact)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise MyException(e, sys)
        


    def start_model_trainer(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        """
        This method of TrainPipeline class is responsible for starting model training
        """
        try:
            model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact,
                                         model_trainer_config=self.model_trainer_config
                                         )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise MyException(e, sys)
        

    





    def run_pipeline(self, ) -> None:
        """
        This method of TrainPipeline class is responsible for running complete pipeline
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact, data_validation_artifact=data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
            logging.info("Pipeline run completed successfully")
            
        except Exception as e:
            raise MyException(e, sys)
        