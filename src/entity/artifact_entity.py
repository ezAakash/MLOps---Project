from dataclasses import dataclass

# har component se related aritfact kya aarhe hai voh 
@dataclass
class DataIngestionArtifact:
    trained_file_path:str 
    test_file_path:str

@dataclass #isko hata ke kuch error aarha tha ....
class DataValidationArtifact:
    validation_status:bool
    message: str
    validation_report_file_path: str
    
@dataclass
class DataTransformationArtifact:
    transformed_object_file_path:str 
    transformed_train_file_path:str
    transformed_test_file_path:str

    