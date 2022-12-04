import click
import pandas as pd
import os
import pickle
import json
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error


@click.command()
@click.option("--dir_model")
@click.option("--test_dir")
@click.option("--dir_save")
def validate(
        dir_model: str, test_dir: str, dir_save: str
):
    X_test = pd.read_csv(os.path.join(test_dir, "features.csv"))
    y_test = pd.read_csv(os.path.join(test_dir, "targets.csv"))
    with open(os.path.join(dir_model, "model.pickle"), 'rb') as f:
        clf = pickle.load(f)

    y_pred = clf.predict(X_test)
    metrics = dict()
    metrics["MAE"] = mean_absolute_error(y_test, y_pred)
    metrics["MSE"] = mean_squared_error(y_test, y_pred)

    path = os.path.join(dir_save, "metrics.json")
    with open(path, "w") as f:
        json.dump(metrics, f, indent=2)


if __name__ == '__main__':
    validate()
