import os
from datetime import timedelta

from airflow import DAG
from airflow.sensors.python import PythonSensor
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.utils.dates import days_ago
from docker.types import Mount


DATA_DIR = "/data/{{ yesterday_ds }}/processed"
MODEL_DIR = "/data/model"
PREDICT_DIR = "/data/{{ yesterday_ds }}/predictions"


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

def wait_for_model(file_path: str):
    return os.path.exists(file_path)

with DAG(
        "inference_pipeline",
        default_args=default_args,
        schedule_interval="@daily",
        start_date=days_ago(5),
) as dag:
    wait = PythonSensor(
        task_id="wait_for_model",
        python_callable=wait_for_model,
        op_kwargs={'file_path': "data/model/model.pickle"},
        timeout=6000,
        poke_interval=10,
        retries=100,
        mode="poke",
    )

    predict = DockerOperator(
        image="airflow-predict",
        command=f"--dir_model {MODEL_DIR} --data_dir {DATA_DIR} --dir_save {PREDICT_DIR}",
        network_mode="bridge",
        task_id="docker-airflow-predict",
        do_xcom_push=False,
        mount_tmp_dir=False,
        mounts=MOUNT_OBJ
    )

    wait >> predict
