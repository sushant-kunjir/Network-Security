
1: find Problem statement and required solution
2: gather the required data
3: create a architecture diagrame for this project 
4: generate a project layout:
    in that we create a files & folders like:
    1.networksecurity:
        it consist all the ml or coding folders like:
            1.components
            2.constants
            3.entity
            4.exception
            5.logging
            6.pipeline
            7.utils
    
    2. .github
        it consists main.yml file
    
    3. .gitignore
        if we writen any file name in that file it skip that file from pushing into github

    4. setup.py
        It is used by setuptools (or distutils in older Python versions) to define the configuration of your project, such as its metadata, dependencies, and more

    5. requirements.txt
        it consits all the required libraries 
    
    6. README.md

    7. .env
        in this file we wrote the required paths for enviroment 
        eg mongo_db_url
    
    8. test_mongo_db.py
        we use this file to check the connectivity with MONGODB

    9. push_data.py
        in this file we wrote a code for pushing the data from local file to mongodb

    10.app.py
    11. main.py

lets see what we did step-by-step
# connectivity with mondodb and inserting data into mongodb
1) we create a cluster in mongodb and copy the connectivity string in .env file 
2) then we check the connectivity by running the test_mongodb.py
3) after that we push our data from local file to mongodb using push_data.py file
    in this file
    1) we take our MONGODB_url using os.getenv() function
    2) the create a network data extract class
    3) in that we create a function csv_to_json_convertor to convert the csv data into json format
    4) then create another function insert_data_mongodb to insert that data into mongodb
    5) after that we call main function in that we initialize the database name,collection name,              raw_data_filepath

# start writing the ML files 
1) networksecurity\constant\training_pipeline\__init__.py:
    in this file we define all the constants which we will give to our files 
    eg TRAIN_FILE_NAME, TEST_FILE_NAME, DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME, ect

1) exception/exception.py:
    in this we create a NetworkSecurityException class which handles the exception if occures

2) logging/logger.py:
    this file returns the logging info

3) networksecurity/constant/training_pipeline/__init__.py
    in this file we define some parameters like:

    1) defining common constant variable for training pipeline :
        TARGET_COLUMN, PIPELINE_NAME, ARTIFACT_DIR, FILE_NAME, TRAIN_FILE_NAME, TEST_FILE_NAME,SCHEMA_FILE_PATH, SAVED_MODEL_DIR, MODEL_FILE_NAME

    2) Data Ingestion related constant start with DATA_INGESTION VAR NAME
        DATA_INGESTION_COLLECTION_NAME, DATA_INGESTION_DATABASE_NAME, DATA_INGESTION_DIR_NAME, DATA_INGESTION_FEATURE_STORE_DIR, DATA_INGESTION_INGESTED_DIR, DATA_INGESTION_TRAIN_TEST_SPLIT_RATION

    3) Data Validation related constant start with DATA_VALIDATION VAR NAME
        DATA_VALIDATION_DIR_NAME, DATA_VALIDATION_VALID_DIR, DATA_VALIDATION_INVALID_DIR, DATA_VALIDATION_DRIFT_REPORT_DIR, DATA_VALIDATION_DRIFT_REPORT_FILE_NAME, PREPROCESSING_OBJECT_FILE_NAME

    4) Data Transformation related constant start with DATA_TRANSFORMATION VAR NAME
        DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
        DATA_TRANSFORMATION_DIR_NAME, DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,DATA_TRANSFORMATION_IMPUTER_PARAMS,DATA_TRANSFORMATION_TRAIN_FILE_PATH,DATA_TRANSFORMATION_TEST_FILE_PATH

    5) Model Trainer ralated constant start with MODE TRAINER VAR NAME
        MODEL_TRAINER_DIR_NAME,MODEL_TRAINER_TRAINED_MODEL_DIR,MODEL_TRAINER_TRAINED_MODEL_NAME,MODEL_TRAINER_EXPECTED_SCORE,MODEL_TRAINER_OVER_FIITING_UNDER_FITTING_THRESHOLD,TRAINING_BUCKET_NAME

4) networksecurity/entity:
    in this we create two files
    1) config_entity.py:
        this file consists an information about the configuration
        in this we create classes for TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig 
        all this classes consist configuration paths/things which initialize in constant/training_pipeline/__init__.py file

    2) artifact_entity.py:
        this file consists an information about artifact folder or how to store the output given by each component file

5) components/data_ingestion.py:
    1) in this first we import all required libraries or dependecies
    2) then we get mongodb_url using os.getenv() function
    3) after that we create a DataIngestion class which consists some functions:
        1)  __init__ : for initialize the DataIngestionConfig written inside the config_entity.py file
        2) export_collection_as_dataframe :
            - it create mongodb client using MONGODB_URL 
            - this function takes database_name and collection_name from data_ingestion_config and access records using mongodb client
            - then that records converted into dataframe
        3) export_data_into_feature_store:
            - this function creates a directory and store that dataframe into it in csv format
        4) split_data_as_train_test:
            - it splits the data into train and test dataset
            - then store train data into training file and test data into testing file
        5) initiate_data_ingestion:
            - this function calls above functions one-by-one
            - first call export_collection_as_dataframe and create dataframe
            - then call export_data_into_feature_store(dataframe) for feature store
            - after that it call split_data_as_train_test to split the data
            - then create variable dataingestionartifact which gives train and test file paths
            - at the end this function returns dataingestionartifact

6) data_schema/schema.yaml:
    schema is used to understand the dataset
    this schema is used to validate the the data in validation.py
    this file consists column names and datatypes in key value pairs
    also consist numerical column names

7) components/data_validation.py:
    1) to validate the data we needs to read yaml file 
    2) thats why we create a function read_yaml_file,write_yaml_file inside "utils.main_utils.utils"
    3) in this file we create a class DataValidation which consists functions like:

        1)  __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig): 
                 
            - it takes dataingestionartifact as input
            - gives datavalidationartifact as output

        2)  read_data(file_path)->pd.DataFrame:
            - it reads file and return dataframe

        3) validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
            it checks the number of columns of dataframe and schema and gives true or ffalse

        4) detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
            - this function detects drift
            - it uses ks_2samp for checking distrbution between base dataframe and current dataframe and store in is_same_dist
            - then if thresold<=is_same_dist.pvalue then is_found=False
            - else is_found=True, status=False
            - then insert pvalue and is_found in report
            - and use write_yaml_file function to update existing yaml file

        5) initiate_data_validation(self)->DataValidationArtifact:
            - it reads train and test file
            - then  validate number of columns and set status
            - then check datadrift
            - saves train and test data 
            - creates data_validation_artifact
            - return data_validation_artifact

8) components/data_transformation.py:
    1) this file reads the data from train and test file, perform some transmation on it and save the data into test.npy and train.npy file
    2) train.npy and test.npy are the files that stores the data into numpy-array format
    3) for saving numpy array data we create a function "save_numpy_array_data" in utils.py  
    4) for saving object we create anothe function "save_object" in ssame file
    5) SMOTETomek: this feature is able to handle the imbalance dataset
    6) In this file we use "KNNImputer" for handling missing/nan values
    7) we initialize DATA_TRANSFORMATION_IMPUTER_PARAMS in constant/training_pipeline/__init__.py for hyperparameter tuning
    8) then we create a class DataTransformation we consists some functions like:

        1)  __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTransformationConfig):
            - takes  DataValidationArtifact as input and initialize DataTransformationConfig 

        2) read_data(file_path) -> pd.DataFrame: 
            - this funcction reads the file convert it into dataframe

        3) get_data_transformer_object(cls)->Pipeline:
            - It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
            and returns a Pipeline object with the KNNImputer object as the first step.
            - Args:
                cls: DataTransformation
            - returns:
                A Pipeline object
        
        4) initiate_data_transformation(self)->DataTransformationArtifact:
            - this function reads training and testing file
            - creates input and target features for both train and test data
            - since in our dataset we have 1 and -1 as target so we convert -1 with 0
            - then we call get_data_transformer_object function as preprocessor
            - then do fit transform training and testing data
            - after that we concatenate input and target feature using np.c_
            - then saves train and test data as numpy array using save_numpy_array_data() function
            - saves the preprocessor object as preprocessor.pkl
            - then create data_transformation_artifact() and return it
        
9) components/model_trainer.py:
    1) we create load_object() and load_numpy_array_data() for loading purpose inside the main_utils.utils.py file
    2) we create  new folder inside utils named as ml_util and inside that folder we again create two new folders as model and metric
    3) inside model we create estimator.py file which takes model and preprocessor, transform values using that and predict the new values
    4) inside metric we create classification_metric.py file which return the f1, precision and recall score 
    5) for evaluating the performance of the model we create evaluate model function inside the utils.py 

    6) inside model_trainer.py file we import some important libraries such as mlflow,dagshub

    7) we connect our github repository with dagshub 
    8) inside  model_trainer.py we create a class modeltrainer which consist functions like:

        1) __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifact):
            it takes DataTransformationArtifact as input and initialize ModelTrainerConfig

        2) track_mlflow(self,best_model,classificationmetric):
            - MLFLOW: it is an open source tool which is use for managing the lifecycle of data-science project
            to see the MLFLOW report we run - "mlflow ui" command
            - DAGsHub: instead of showing mlflows output locally we connect github repository with dagshub and show it there
            - then we set mlflow registry uri (dagshub) and start mlflow run

        3) train_model(self,X_train,y_train,x_test,y_test):
            - this function trains the model
            - inside it we firstly create model list and params list 
            - then call evaluate_models function and take best model with high score from it 
            - after that we predict the values for x_train & y_train data and call get_classification_score() function 
            - then Track the experiements with mlflow
            - after that we load preprocessor using load_object() function
            - then we create Network_Model using preprocessor and best model and save it 
            - we also save the best model in model.pkl file
            - then we create model_trainer_artifact and return it 
        
        4) initiate_model_trainer(self)->ModelTrainerArtifact:
            - this function initiate the model trainer 
            - it reads the data from output of data_transformation.py (train.npy, test.npy) by using load_numpy_array_data() function
            - then splits the data into x_train, y_train, x_test, y_test
            - then call train_model() for taking model_trainer_artifact 
            - at the end it return model_trainer_artifact

    9) since our all important files (like model.pkl, preprocessor.pkl) are in artifact folder we need to push it to a single folder from which we can access it for future purpose 
    therefore we write a code like save_object("final_model/model.pkl",best_model) as a model pusher


10) pipeline/training_pipeline.py:
    1) this file is responsible for initiating our project
    2) inside this file we create a trainingpipeline class which have functions like:
        1) _init__(self):
        2) start_data_ingestion(self):
        3) start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        4) start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        5) def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        6) sync_artifact_dir_to_s3(self):
        7) sync_saved_model_dir_to_s3(self):
        8) run_pipeline(self):
    3) create s3_syncer.py file and create functions:
        sync_folder_to_s3(): for synce from folder to s3
        sync_folder_from_s3(): for synce folder from s3
  
11) app.py :
    - for checking all files are working or not we create an app.py file using fastapi
    - create apis for train and predict 

12) aws :
    1) IAM: create aws IAM and connect it with our command promt using access keys and screte key
    2) S3: create s3 bucket with name networksecurity34 and paste that bucket name into init file
    3) ECR: create ECR 
    4) create EC2 for deployment 

13) run app using : uvicorn app:app --reload

14) Building DockerImage and Github actions

    1) create docker file
    2) .github/workflows/main.yml
        - create workflow name
        - starts creating jobs
            1) continuous integration
            2) build and push ecr image
            3) continuos deployment

15) creating security credentials in Github 
    Setup github secrets:

        <!-- AWS_ACCESS_KEY_ID= 

        AWS_SECRET_ACCESS_KEY= 

        AWS_REGION = us-east-1

        AWS_ECR_LOGIN_URI = 566167302285.dkr.ecr.us-east-1.amazonaws.com/networksecurity

        ECR_REPOSITORY_NAME = networksecurity -->
    
16) in EC2 instance :
    use linux 
    after that use given commands to run that EC2 instance 

        Docker Setup In EC2 commands to be Executed
        #optinal

        sudo apt-get update -y

        sudo apt-get upgrade

        #required

        curl -fsSL https://get.docker.com -o get-docker.sh

        sudo sh get-docker.sh

        sudo usermod -aG docker ubuntu

        newgrp docker















