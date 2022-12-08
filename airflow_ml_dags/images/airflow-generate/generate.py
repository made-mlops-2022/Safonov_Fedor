import click
import pandas as pd
import numpy as np
import os
from sklearn.datasets import load_wine


N = 100


def get_df_sample():
    data = load_wine()
    df = pd.DataFrame(data=data.data, columns=data.feature_names)
    df['target'] = pd.Series(data.target)
    return df


@click.command()
@click.argument("output_dir")
def generate(output_dir: str):
    df_sample = get_df_sample()
    n_cols = len(df_sample.columns)

    # Создаем папку с нужной датой
    pathes = os.path.split(output_dir)
    os.makedirs(pathes[0], exist_ok=True)

    data = np.random.rand(N, n_cols)
    data[:, -1] = np.random.randint(0, 3, N)
    df_new = pd.DataFrame(data=data, columns=df_sample.columns)
    df_new.to_csv(output_dir, index=False)


if __name__ == '__main__':
    generate()
