import click
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import MinMaxScaler


@click.command()
@click.option("--input-dir")
@click.option("--output-dir")
def preprocess(input_dir: str, output_dir: str):
    data = pd.read_csv(os.path.join(input_dir, "data.csv"))
    columns = data.columns
    data_proc = data.drop(columns=["target"])

    # Тут должна быть функция приведения сырых данных в нужный нам вид
    transformer = MinMaxScaler(feature_range=(0, 100), clip=False)
    data_proc = pd.DataFrame(transformer.fit_transform(data_proc), columns=columns[:-1])
    data_proc["target"] = data["target"]

    os.makedirs(output_dir, exist_ok=True)
    data_proc.to_csv(os.path.join(output_dir, "data.csv"), index=False)


if __name__ == '__main__':
    preprocess()
