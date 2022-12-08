import os
from datetime import timedelta

from airflow import DAG
from airflow.sensors.python import PythonSensor
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount

INPUT_DATA_DIR = "/data/{{ yesterday_ds }}/processed"
TRAIN_DIR = "/data/{{ yesterday_ds }}/train"
TEST_DIR = "/data/{{ yesterday_ds }}/test"
MODEL_DIR = "/data/model"
METRICS_DIR = "/data/{{ yesterday_ds }}/model"

default_args = {
    "owner": "airflow",
    "email": ["safonovfedya696@gmail.com"],
    'retry_exponential_backoff': True,
    'retry_delay': timedelta(seconds=10),
    "retries": 1,
}

MOUNT_OBJ = [Mount(
    source="/home/fedor/Future/VK/2 сем/MLOps/HWS_MAIN/Safonov_Fedor/airflow_ml_dags/data",
    target="/data",
    type='bind'
    )]

def wait_for_file(file_path: str):
    return os.path.exists(file_path)

with DAG(
        "train_pipeline",
        default_args=default_args,
        schedule_interval="@weekly",
        start_date=days_ago(5),
) as dag:
    wait = PythonSensor(
        task_id="wait_for_file",
        python_callable=wait_for_file,
        op_kwargs={'file_path': "data/{{ yesterday_ds }}/processed/data.csv"},
        timeout=6000,
        poke_interval=10,
        retries=100,
        mode="poke",
    )

    split = DockerOperator(
        image="airflow-split",
        command=f"--input_dir {INPUT_DATA_DIR} --dir_train {TRAIN_DIR} --dir_test {TEST_DIR}",
        network_mode="bridge",
        task_id="docker-airflow-split",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=MOUNT_OBJ
    )

    train = DockerOperator(
        image="airflow-train",
        command=f"--dir_train {TRAIN_DIR} --dir_save {MODEL_DIR}",
        network_mode="bridge",
        task_id="docker-airflow-train",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=MOUNT_OBJ
    )

    validate = DockerOperator(
        image="airflow-validate",
        command=f"--dir_model {MODEL_DIR} --test_dir {TEST_DIR} --dir_save {MODEL_DIR}",
        network_mode="bridge",
        task_id="docker-airflow-validate",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=MOUNT_OBJ
    )

    wait >> split >> train >> validate
