from flask import Flask
import pickle
import os
import pandas as pd

# dicionário para os tipos de métodos experimentais
# experimentalTechnique = 
# 'XRAYDIFFRACTION': 0
# 'POWDERDIFFRACTION': 1
# 'ELECTRONCRYSTALLOGRAPHY': 2
# 'NEUTRONDIFFRACTION': 3 
# 'XRAYDIFFRACTIONEPR': 4
# 'EPRXRAYDIFFRACTION': 5
# 'NEUTRONDIFFRACTIONXRAYDIFFRACTION': 6
# 'XRAYDIFFRACTIONNEUTRONDIFFRACTION': 7
# 'SOLUTIONSCATTERINGXRAYDIFFRACTION': 8

# Abre e carrega o modelo anteriormente salveo
path = os.path.join(os.path.dirname(__file__), 'classificadorProteinas.pkl')
modelo = pickle.load(open(path, 'rb'))

# Gera a aplicação flask
app = Flask(__name__)

@app.route("/")
def inicial():
    return "Caminho raiz, use /predict e faça o input dos dados para predizer a estrutura"

@app.route("/predict/<experimentalTechnique>/<resolution>/<structureMolecularWeight>/<crystallizationTempK>/<densityPercentSol>/<phValue>")
def predict_label(experimentalTechnique, resolution, structureMolecularWeight, crystallizationTempK, densityPercentSol, phValue):

    # Recebe os dados da url do endpoint e prepara para previsão
    dados = {
        'experimentalTechnique': [experimentalTechnique],
        'resolution': [resolution],
        'structureMolecularWeight': [structureMolecularWeight],
        'crystallizationTempK': [crystallizationTempK],
        'densityPercentSol': [densityPercentSol],
        'phValue': [phValue]
    }
    df_predicao = pd.DataFrame(dados)
    
    try:
        # Realiza a previsão e transforma o output no label
        cd_proteina = modelo.predict(df_predicao)
        if cd_proteina[0] == 0:
            label = "OXIDOREDUCTASE"
        elif cd_proteina[0] == 1:
            label = "TRANSFERASE"
        elif cd_proteina[0] == 2:
            label = "HYDROLASE"
        elif cd_proteina[0] == 3:
            label = "IMMUNESYSTEM"
        elif cd_proteina[0] == 4:
            label = "RIBOSOME"
        response = f"Classificação da prevista: {label}"

    except Exception as e:
        response = f"Erro na classificação {e}"
    
    return response

if __name__ == "__main__":
    app.run(debug=True)