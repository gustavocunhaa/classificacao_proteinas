# 🧬 Protein Data Bank

Repositório contendo o projeto de um pequeno data lake com um conjunto de dados sobre proteínas, disponibilizados pelo https://www.rcsb.org/.

> Dados disponíveis em -> https://www.kaggle.com/datasets/shahir/protein-data-set

<div style="display: inline_block"><br>
  <img align="center" alt="kaggle" height="60" width="70" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/kaggle/kaggle-original-wordmark.svg">   
  <img align="center" alt="python" height="60" width="70" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg">
  <img align="center" alt="pandas" height="60" width="70" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pandas/pandas-original.svg">
  <img align="center" alt="aws" height="60" width="70" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg">
  <img align="center" alt="s3" height="60" width="70" src="https://cdn.worldvectorlogo.com/logos/amazon-s3-simple-storage-service.svg">
  <img align="center" alt="mysql" height="60" width="70" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original-wordmark.svg">
  <img align="center" alt="sklearn" height="60" width="70" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/scikitlearn/scikitlearn-original.svg"> 
  <img align="center" alt="fastapi" height="60" width="70" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original-wordmark.svg">
  <img align="center" alt="streamlit" height="60" width="70" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/streamlit/streamlit-original.svg"> 
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

 Iniciando o serviço de API localmente da pasta root do proejto:
``` cmd:
fastapi dev app/endpoint.py
```

# Comparativo entre input dos modelos

Como experimento, dois modelos com o mesmo target foram treinados, porém com inputs diferentes. A diferença entre os dois modelos em perfôrmance mostra que a combinação input + modelo sempre seŕa mais assertiva com base na necessidade e nos detalhes do dataset. Não existe "bala de prata" que resolva um problema de ML.  

- lab_feature : O modelo recebeu como input os dados de testes e parâmetros físico químicos da macromolécula.
- sequence_feature: O modelo recebeu aqui a sequência da macromolécula, especificando as 5 primeiras bases.