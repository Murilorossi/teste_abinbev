# Pipeline Airflow com PySpark e Docker

## Resumo
Este projeto faz um ETL a partir de uma API de cervejarias.

## Arquitetura
- **Bronze:** Dados sem alterações salvo em json.
- **Prata:** Dados tratados e particionado por 'state' e armazenado em parquet.
- **Ouro:** Dados agregados por 'state', 'brewery_type' e count salvos em parquet.

## Requisitos
Docker e Docker Compose instalado no computador.

## Passo a passo
- Clone o repositorio https://github.com/Murilorossi/teste_abinbev.git
- Abra o terminal na pasta do projeto use o comando "docker-compose up --build -d"
- Acesse "localhost:8080"
- faça o login usando username: admin password: admin
- execute a DAG, clicando em trigger DAG
- Caso queira testar o envio de email em caso de falha, altere o email e senha no arquivo (no exemplo @outlook) no arquivo docker-composer.yml
