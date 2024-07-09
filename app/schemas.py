from pydantic import BaseModel

class LabFeatures(BaseModel):
    temperatura_cristalizacao_k: int
    contagem_residuos: int
    medida_de_resolucao: float
    peso_molecular: float
    ph: float
    densidade_percentual_solucao: float
