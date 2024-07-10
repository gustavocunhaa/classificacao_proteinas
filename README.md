# 🧬 Protein Data Bank

Repositório contendo o projeto de um pequeno data lake com um conjunto de dados sobre proteínas, disponibilizados pelo https://www.rcsb.org/.

> Dados disponíveis em -> https://www.kaggle.com/datasets/shahir/protein-data-set

<div style="display: inline_block"><br>
  <img align="center" alt="kaggle" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/kaggle/kaggle-original-wordmark.svg">   
  <img align="center" alt="python" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg">
  <img align="center" alt="pandas" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg">
  <img align="center" alt="aws" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg">
  <img align="center" alt="s3" height="50" width="60" src="https://cdn.worldvectorlogo.com/logos/amazon-s3-simple-storage-service.svg">
  <img align="center" alt="mysql" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original-wordmark.svg">
  <img align="center" alt="sklearn" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/scikitlearn/scikitlearn-original.svg"> 
  <img align="center" alt="fastapi" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original-wordmark.svg">
  <img align="center" alt="streamlit" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/streamlit/streamlit-original.svg"> 
</div>       


# Conteúdo:
1. Pipeline de extração, obtenção e disponibilização do dado para consumo
2. Modelo de classificação da estrutura com base em resultados de testes laboratoriais
3. API para consumo da previsão dos modelos
 
# Estrutura do projeto

- **app**: Contém a api de consumo final dos modelos
- **data**: Pasta para armazenamento dos arquivos de dados temporários durante o preocessamento
- **docs**: Documentações do projeto
- **src**: Local com os recursos utilizados pelas aplicações
- **example.env**: Local com o exemplo do arquivo .env demonstrando como armazenar as credenciais utilizadas pelo projeto


# Arquitetura do projeto

### Pipeline de dados
- Utilização do AWS s3 para armazenar os arquivos pelas camadas
- Contrução em três níveis de granularidade do dado
- Banco SQL final para consumo do dado tratado

![arch](./docs/img/arch.png)


 Banco relacional:
![database](./docs/img/database.png)


### Pipeline de Machine Learning
- Os dados são extraídos por python utilizando SQL
- Os dados são tratados como features para treinamento do modelo de Machine Learning
- O modelo é serializado e disponibilizado com uma camada de API
- A API é utilizada para alimentar uma ferramenta de visualização facilitando a utilização e experimentação das previsões

![arch_ml](./docs/img/arch_ml.jpg)


# API para consumo das previsões

A API foi desenvolvida utilizando o framework do FastAPI, pois é de fácil uso e agrega algumas funcionalidades de forma automática, como é o caso da documentação dos endpoints.

 Iniciando o serviço de API localmente da pasta raiz do proejto:
``` cmd:
fastapi dev api.py
```
☁️ Deploy da API foi feito utilizando plano free do [Render](https://render.com/)

> https://classificacao-proteinas.onrender.com/docs


# Comparativo entre input dos modelos

Como experimento, dois modelos com o mesmo target foram treinados, porém com inputs diferentes. 

A diferença entre os dois modelos em perfôrmance mostra como que a qualidade dos dados de input refletem na qualidade dos outputs previstos. Não existe "bala de prata" que resolva todos os problema possíveis de ML.

- lab_feature : O modelo recebeu como input os dados de testes e parâmetros físico químicos da macromolécula.
- sequence_feature: O modelo recebeu como input a sequência da macromolécula.

Resultados:

![model](./docs/img/model_newplot.png)


 Iniciando o painel de visualização localmente da pasta raiz do proejto:
``` cmd:
streamlit run dashboard.py
```
☁️ Deploy utilizando a própria infra disponibilizada pelo [Streamlit](https://share.streamlit.io/deploy)

> https://gustavocunhaa-classificacaoproteinas.streamlit.app