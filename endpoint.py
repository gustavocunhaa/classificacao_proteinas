from flask import Flask, request
import pickle
import os

# dicionário para os tipos de métodos experimentais
# metodo_experimental = 
# 'XRAYDIFFRACTION': 0
# 'POWDERDIFFRACTION': 1
# 'ELECTRONCRYSTALLOGRAPHY': 2
# 'NEUTRONDIFFRACTION': 3 
# 'XRAYDIFFRACTIONEPR': 4
# 'EPRXRAYDIFFRACTION': 5
# 'NEUTRONDIFFRACTIONXRAYDIFFRACTION': 6
# 'XRAYDIFFRACTIONNEUTRONDIFFRACTION': 7
# 'SOLUTIONSCATTERINGXRAYDIFFRACTION': 8

dic_dados = [
    'experimentalTechnique',
    'resolution',
    'structureMolecularWeight',
    'crystallizationTempK',
    'phValue'
]

path = os.path.join(os.path.dirname(__file__), 'classificadorProteinas.sav')
modelo = pickle.load(open(path, 'rb'))

app = Flask(__name__)

@app.route('/', methods=['POST'])
def classifier():
    dados = request.get_json()
    dados_input = [dados[col] for col in dic_dados]
    cd_proteina = modelo.predict([dados_input])
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
    return str(label)

app.run(debug=True)