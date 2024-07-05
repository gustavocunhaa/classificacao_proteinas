from pydantic import BaseModel

class StructureModel(BaseModel):
    temperatura_cristalizacao_k: list[int]
    contagem_residuos: list[int]
    medida_de_resolucao: list[float]
    peso_molecular: list[float]
    ph: list[float]
    densidade_percentual_solucao: list[float]
