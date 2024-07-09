import os
from pathlib import Path
from dotenv import load_dotenv

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
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
DATASET_PATH = Path(f"{ROOT_PATH}/src/ml/sqls/dataset_sequence.sql")
MODEL_SAVE_PATH = Path(f"{ROOT_PATH}/src/ml/model")

# PARAMS
query = open(DATASET_PATH, 'r').read()
model_name = 'sequence_feature'
test_size = 0.2
model_pipeline = Pipeline([
    ('vectorize', CountVectorizer()),
    ('clf', DecisionTreeClassifier(random_state=1337))
])

# MAIN EXEC
df = ReadDatabase(
    user=mysql_credentials['user'],
    password=mysql_credentials['pwd'],
    host=mysql_credentials['host'],
    port=mysql_credentials['port'],
    database=mysql_credentials['db'],
    data_query=query
).run()

TrainTestModel(
    model_name=model_name,
    x=df['sequencia'],
    y=df['y'],
    test_size=test_size,
    model=model_pipeline,
    path_save=MODEL_SAVE_PATH
).run()