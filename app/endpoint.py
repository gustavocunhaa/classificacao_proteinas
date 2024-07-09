from fastapi import FastAPI

from schemas import LabFeatures
from model.lab_feature import model_predict


app = FastAPI()


@app.get("/")
async def root():
    return "API predict models service. Try /docs"


@app.post("/predict/lab/")
async def lab_feature_model(data: LabFeatures):
    body = data.model_dump_json()
    response = model_predict(body)
    return response