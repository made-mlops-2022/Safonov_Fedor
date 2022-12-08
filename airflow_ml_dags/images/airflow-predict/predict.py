import click
import pandas as pd
import os
import pickle
import json
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error


@click.command()
@click.option("--dir_model")
@click.option("--data_dir")
@click.option("--dir_save")
def predict(
        dir_model: str, data_dir: str, dir_save: str
):
    data = pd.read_csv(os.path.join(data_dir, "data.csv"))
    X_test = data.drop(columns=["target"])
    with open(os.path.join(dir_model, "model.pickle"), 'rb') as f:
        clf = pickle.load(f)

    y_pred = clf.predict(X_test)
    df_result = pd.DataFrame(y_pred, columns=["target"])
    os.makedirs(dir_save, exist_ok=True)
    path = os.path.join(dir_save, "predictions.csv")
    df_result.to_csv(path, index=False)


if __name__ == '__main__':
    predict()
