import os
from datetime import timedelta

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

default_args = {
    "owner": "airflow",
    "email": ["airflow@example.com"],
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

MOUNT_OBJ = [Mount(
    source="/home/fedor/Future/VK/2 сем/MLOps/HWS_MAIN/Safonov_Fedor/airflow_ml_dags/data",
    target="/data",
    type='bind'
    )]

with DAG(
        "generate_data",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=days_ago(5),
) as dag:
    generate = DockerOperator(
        image="airflow-generate",  # Имя контейнера
        command="/data/{{ yesterday_ds }}/raw/data.csv",  # Параметр скрипта
        network_mode="bridge",  # Соединяем локальную dir с dir в докере
        task_id="docker-airflow-generate",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=MOUNT_OBJ
    )

    preprocess = DockerOperator(
        image="airflow-preprocess",
        command="--input-dir /data/{{ yesterday_ds }}/raw --output-dir /data/{{ yesterday_ds }}/processed",
        task_id="docker-airflow-preprocess",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=MOUNT_OBJ
    )

    generate >> preprocess
