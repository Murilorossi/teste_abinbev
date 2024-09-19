from pyspark.sql.functions import count
from datetime import datetime
import os


def transformar_dados_ouro(spark):
    """
    A função carrega os dados particionados por estado da camada Silver, realiza uma agregação para contar
    o numero de cervejarias por tipo e estado depois salva o resultado na camada gold no formato parquet

    Parâmetros:
    spark: instância do SparkSession para a leitura e manipulação dos dados.

    Exceções:
        Se não tiver dados na camada Silver.
        Se não tiver dados disponíveis para agregação.
    """

    # Gera data atual para nomeação do arquivo
    date_str = datetime.now().strftime('%Y_%m_%d')
    silver_dir = f"/opt/airflow/data/silver"
    gold_dir = f"/opt/airflow/data/gold"

    # Verifica se o arquivo da camada prata existe
    if os.path.exists(f"{silver_dir}/cervejarias_{date_str}.parquet"):
        df = spark.read.parquet(f"{silver_dir}/cervejarias_{date_str}.parquet")

        # Agrupa os dados
        agg_data = df.groupBy("state", "brewery_type").agg(count("*").alias("brewery_count"))

        # Cria o diretorio da camada ouro
        os.makedirs(gold_dir, exist_ok=True)

        # Salva os dados agregados na camada ouro
        agg_data.write.mode("overwrite").parquet(f"{gold_dir}/cervejarias_{date_str}.parquet")

        print(f"Dados agregados e salvos na camada Ouro em {gold_dir}")
    else:
        raise FileNotFoundError(f"O arquivo {silver_dir}/cervejarias_{date_str}.parquet não foi encontrado.")

