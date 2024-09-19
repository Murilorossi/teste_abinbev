from datetime import datetime
import os


def transformar_dados_prata(spark):
    """
    A função carrega os dados da camada Bronze, realiza uma transformação para particionar os dados por estado
    e salva os dados no formato parquet na camada Silver

    Parâmetros:
    spark: instância do SparkSession para a leitura e manipulação dos dados.

    Exceções:
        - Se o arquivo JSON da camada Bronze não for encontrado, levanta um erro
    """

    # Gera data atual para nomeação do arquivo
    date_str = datetime.now().strftime('%Y_%m_%d')
    bronze_path = f"/opt/airflow/data/bronze/cervejarias_{date_str}.json"

    # Verifica se o arquivo existe na camada bronze
    if os.path.exists(bronze_path):
        df = spark.read.json(bronze_path)

        # Remove a coluna que tem valores nulos em todos os registros
        df = df.drop('address_3')

        # Salvando dados transformados na camada prata
        silver_dir = f"/opt/airflow/data/silver"
        df.write.partitionBy("state").mode("overwrite").parquet(f"{silver_dir}/cervejarias_{date_str}.parquet")

        print(f"Dados transformados e salvos na camada Prata em {silver_dir}")
    else:
        raise FileNotFoundError(f"O arquivo {bronze_path} não foi encontrado.")
