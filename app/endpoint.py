from fastapi import FastAPI

from schemas import LabFeatures, SequenceFeatures
from model.lab_feature      import model_predict as lab_predict
from model.sequence_feature import model_predict as sequence_predict

app = FastAPI()


@app.get("/")
async def root():
    return "API predict models service. Try /docs"


@app.post("/predict/lab/")
async def lab_feature_model(data: LabFeatures):
    body = data.model_dump_json()
    response = lab_predict(body)
    return response

@app.post("/predict/sequence/")
async def lab_feature_model(data: SequenceFeatures):
    body = data.model_dump_json()
    response = sequence_predict(body)
    return response