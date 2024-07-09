import os
from pathlib import Path

import json
import pickle

import pandas as pd

ROOT_PATH  = os.getcwd()
MODEL_PATH = Path(f"{ROOT_PATH}/src/ml/model/sequence_feature/model_1720544357.pkl")

model = pickle.load(open(MODEL_PATH, 'rb'))

def clasify_structure(id_structure: int):
    if id_structure == 0:
        structure = 'HYDROLASE'
    elif id_structure == 1:
        structure = 'TRANSFERASE'
    elif id_structure == 2:
        structure = 'OXIDOREDUCTASE'
    elif id_structure == 3:
        structure = 'LYASE'
    return structure

def model_predict(body: dict):
    x = pd.DataFrame(json.loads(body), index=[0])
    predict = model.predict(x)[0]

    response = {
        'body': json.dumps( {'classification' : clasify_structure(predict)} ),
        'statusCode': 200
    }
    
    return response


