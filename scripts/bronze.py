import requests
import json
import os
from datetime import datetime


def ler_dados_api():
    """
    Função para extrair dados da API e salvar na camada bronze

    Se a requisição for completa, vai criar o diretorio bronze e armazenar os dados em json na camada bronze

    Exceções:
        Se a chamada da API falhar, a função gera uma exceção com o status code retornado
    """

    url = "https://api.openbrewerydb.org/breweries"
    response = requests.get(url)

    # Checando leitura da API
    if response.status_code == 200:
        data = response.json()

        bronze_dir = "/opt/airflow/data/bronze"
        os.makedirs(bronze_dir, exist_ok=True)

        # Salva os dados na camada bronze
        file_path = f"{bronze_dir}/cervejarias_{datetime.now().strftime('%Y_%m_%d')}.json"
        with open(file_path, 'w') as f:
            json.dump(data, f)

        print(f"Dados salvos com sucesso no arquivo: {file_path}")

    else:
        raise Exception(f"Falha ao ler os dados da API. Status code: {response.status_code}")