import os
from pathlib import Path
import pickle
import json
import pandas as pd
from sklearn.preprocessing import minmax_scale


ROOT_PATH  = os.getcwd()
MODEL_PATH = Path(f"{ROOT_PATH}/src/structure_protein_model/model/structure_protein_classify_1720199724.pkl")

model = pickle.load(open(MODEL_PATH, 'rb'))

def normalize_data(data: dict):
    df = pd.DataFrame(json.loads(data))
    norm = minmax_scale(df, (0,1))
    x = pd.DataFrame(norm, columns=df.columns.to_list())
    return x

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
    x = normalize_data(body)
    predict = model.predict(x)[0]
    proba = model.predict_proba(x).max()

    response = {
        'body': json.dumps({
            'classification' : clasify_structure(predict),
            'proba': str(proba)
            }),
        'statusCode': 200
    }
    
    return response