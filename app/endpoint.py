from fastapi import FastAPI
from structure_model import model_predict
from schemas import StructureModel

app = FastAPI()


@app.get("/")
async def root():
    return "Structure model API service. Try /docs"

@app.post("/structure/")
async def structure_model_predict(data: StructureModel):
    body = data.model_dump_json()
    response = model_predict(body)
    return response