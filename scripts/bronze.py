import requests
import json
import os
from datetime import datetime


def ler_dados_api():
    """
    Função para extrair dados paginados da API e salvar na camada bronze.
    """
    base_url = "https://api.openbrewerydb.org/v1/breweries"
    page = 1
    all_data = []

    while True:
        response = requests.get(base_url, params={"page": page, "per_page": 50})

        if response.status_code == 200:
            data = response.json()
            if not data:
                break

            all_data.extend(data)
            page += 1
        else:
            raise Exception(f"Falha ao ler os dados da API. Status code: {response.status_code}")

    bronze_dir = "/opt/airflow/data/bronze"
    os.makedirs(bronze_dir, exist_ok=True)

    file_path = f"{bronze_dir}/cervejarias_{datetime.now().strftime('%Y_%m_%d')}.json"
    with open(file_path, 'w') as f:
        json.dump(all_data, f)

    print(f"Dados salvos com sucesso no arquivo: {file_path}")
