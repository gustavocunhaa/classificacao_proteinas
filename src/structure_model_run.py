import os
from pathlib import Path
from dotenv import load_dotenv

from xgboost import XGBClassifier

from structure_protein_model.feature_process  import FeatureProcess
from structure_protein_model.train_test_model import TrainTestModel


# LOAD CREDENTIALS FOR .env
load_dotenv()
mysql_credentials = {
    'user': os.getenv("MYSQL_USER"),
    'pwd': os.getenv("MYSQL_PASSWORD"),
    'host': os.getenv("MYSQL_HOST"),
    'port': os.getenv("MYSQL_PORT"),
    'db': os.getenv("MYSQL_DB")
}

# CONSTANTES
ROOT_PATH = os.getcwd()
DATASET_PATH = Path(f"{ROOT_PATH}/src/structure_protein_model/sqls/dataset.sql")
MODEL_SAVE_PATH = Path(f"{ROOT_PATH}/src/structure_protein_model/model")

# PARAMS
query = open(DATASET_PATH, 'r').read()
model_name = 'structure_protein_classify'
target = 'y'
test_size = 0.2
model = XGBClassifier(random_state = 1337, n_estimators = 500)
splits = 5
param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.1, 0.01, 0.001],
    'subsample': [0.5, 0.7, 1]
}
metric = 'f1_weighted'

# MAIN EXEC
df = FeatureProcess(
    user=mysql_credentials['user'],
    password=mysql_credentials['pwd'],
    host=mysql_credentials['host'],
    port=mysql_credentials['port'],
    database=mysql_credentials['db'],
    data_query=query
).run()

TrainTestModel(
    model_name=model_name,
    x=df.drop(columns=[target]),
    y=df[target],
    test_size=test_size,
    model_params=param_grid,
    n_splits=splits,
    otimization_metric=metric,
    model=model,
    path_save=MODEL_SAVE_PATH
).run()
