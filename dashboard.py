from pathlib import Path
import os
import json

import requests as r
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px


# -------------------------
# Painel configs
st.set_page_config(layout= 'wide')

page_title = "🧬 Protein Data Bank: Classificadores de proteínas"
st.markdown(f"# {page_title}")

autor_html = """
<div style="display: inline_block"><br>
  <a href="https://github.com/gustavocunhaa">
    <img align="center" alt="github" height="40" width="50" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/github/github-original-wordmark.svg">
  <a href="https://www.linkedin.com/in/gustavo-cunha-312a80157/">
    <img align="center" alt="linkedin" height="40" width="50" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linkedin/linkedin-original.svg">
  </a>
</div>
""" 


# -------------------------
# API Consume methods

BASE_URL = f"https://classificacao-proteinas.onrender.com/predict"

@st.cache_data
def make_request(url, input):
    headers = {"Content-Type": "application/json"}
    response = r.post(url=url, headers=headers, data=input)
    return response

@st.cache_data
def predict(body, type=['lab', 'sequence']):
    data = json.dumps(body)
    response = make_request(f"{BASE_URL}/{type}", input=data)
    return json.loads(response.content)


# -------------------------
# Pages render

with st.sidebar:    
    selected = option_menu(
        menu_title="Menu",
        options=["Home", "Sequence Models", "Laboratory Models"], 
        icons=['house', 'list-task', 'list-task'],
        menu_icon="cast"
        )
    st.markdown("> [API Docs](https://classificacao-proteinas.onrender.com/docs)")
    st.markdown(f"> **Autor**: Gustavo de Paula Cunha")
    st.html(f"{autor_html}")

if selected == "Home":
    def read_results_json(model):
        path = Path(f"{os.getcwd()}/src/ml/model/{model}.json")
        model_type = model.split("/")[0]
        file = open(path, 'r').read()
        df = pd.DataFrame(json.loads(file), index=["Values"])
        df = df.T
        df["Model Type"] = model_type
        df = df.reset_index().rename(columns={"index":"Metrics"})
        return df

    df = pd.concat([
        read_results_json("sequence_feature/results_1720544357"),
        read_results_json("lab_feature/results_1720537739")
    ])

    fig = px.bar(df, 
                x='Metrics', 
                y='Values', 
                color='Model Type', 
                barmode='group',
                color_discrete_sequence=px.colors.qualitative.Prism,
                title='Models metrics', 
                range_y=[0, 1])
    st.plotly_chart(fig, use_container_width=True)


elif selected == "Sequence Models":
    sequencia = st.text_area(label="sequencia", value="STAGKVIKCKAAVLWEEKKPFSIEEVEVAPPKAHEVRIKMVATGICRSDDHVVSGTLVTPLPVIAGHEAAGIVESIGEGVTTVRPGDKVIPLWTPQCGKCRVCKHPEGNFCLKNDLSMPRGTMQDGTSRFTCRGKPIHHFLGTSTFSQYTVVDEISVAKIDAASPLEKVCLIGCGFSTGYGSAVKVAKVTQGSTCAVFGLGGAGLSVIMGCKAAGAARIIGVDINKDKFAKAKEVGATECVNPQDYKKPIQEVLTEMSNGGVDFSFEVIGRLDTMVTALSCCQEAYGVSVIVGVPPDSQNLSMNPMLLLSGRTWKGAIFGGFKSKDSVPKLVADFMAKKFALDPLITHVLPFEKINEGFDLLRSGESIRTILTF")
    input_seq = {
        "sequencia" : f"{sequencia}"
        }
    st.write("Input data:")
    st.json(input_seq)
    if st.button("Predict Sequence model"):
        value = predict(body=input_seq, type='sequence')
        st.write("Predict value:")
        st.json(value)


elif selected == "Laboratory Models":
    column1, column2 = st.columns([3,3])
    with column1:
        temperatura_cristalizacao_k = st.number_input(label="temperatura_cristalizacao_k", value=277)
        contagem_residuos = st.number_input(label="contagem_residuos", value=347)
        medida_de_resolucao = st.number_input(label="medida_de_resolucao", value=2.6)
    with column2:
        peso_molecular = st.number_input(label="peso_molecular", value=40658.5)
        ph = st.number_input(label="peso_molecular", value=8.4)
        densidade_percentual_solucao = st.number_input(label="densidade_percentual_solucao", value=46.82)
    input_lab = {
        "temperatura_cristalizacao_k" : temperatura_cristalizacao_k,
        "contagem_residuos": contagem_residuos,
        "medida_de_resolucao": medida_de_resolucao,
        "peso_molecular": peso_molecular,
        "ph": ph,
        "densidade_percentual_solucao": densidade_percentual_solucao
        }
    st.write("Input data:")
    st.json(input_lab)
    if st.button("Predict Laboratory model"):
        value = predict(body=input_lab, type='lab')
        st.write("Predict value:")
        st.json(value)
