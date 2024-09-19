FROM apache/airflow:2.4.1

USER root

RUN rm -rf /etc/apt/sources.list.d/mysql.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends openjdk-11-jdk && apt-get clean

COPY ./scripts /scripts
COPY ./dags /dags

USER airflow

RUN pip install pyspark==3.3.1 pyarrow==10.0.1

ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
