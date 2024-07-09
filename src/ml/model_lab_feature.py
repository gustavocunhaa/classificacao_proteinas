import os
from pathlib import Path
from dotenv import load_dotenv

import pandas as pd
from sklearn.preprocessing import minmax_scale
from sklearn.tree import DecisionTreeClassifier

from utils.database_read import ReadDatabase
from utils.train_test_model import TrainTestModel


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
DATASET_PATH = Path(f"{ROOT_PATH}/src/ml/sqls/dataset_lab.sql")
MODEL_SAVE_PATH = Path(f"{ROOT_PATH}/src/ml/model")

# PARAMS
query = open(DATASET_PATH, 'r').read()
model_name = 'lab_feature'
target = 'y'
test_size = 0.2
model = DecisionTreeClassifier(random_state = 1337)
splits = 5
param_grid = {
    "max_depth": [None, 2, 3, 5, 10, 20],
    "min_samples_leaf": [2, 5, 10, 20, 50, 100],
    "criterion": ["gini", "entropy"]
}
metric = 'f1_weighted'

# MAIN EXEC
df = ReadDatabase(
    user=mysql_credentials['user'],
    password=mysql_credentials['pwd'],
    host=mysql_credentials['host'],
    port=mysql_credentials['port'],
    database=mysql_credentials['db'],
    data_query=query
).run()

features = df.drop(columns=['y'])
x = pd.DataFrame(
    minmax_scale(features, (0,1)),
    columns=features.columns.to_list()
)

TrainTestModel(
    model_name=model_name,
    x=x,
    y=df[target],
    test_size=test_size,
    grid_search=True,
    model_params=param_grid,
    n_splits=splits,
    otimization_metric=metric,
    model=model,
    path_save=MODEL_SAVE_PATH
).run()