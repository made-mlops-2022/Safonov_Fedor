import click
import pandas as pd
import os
from sklearn.model_selection import train_test_split


@click.command()
@click.option("--input_dir")
@click.option("--dir_train")
@click.option("--dir_test")
def split(
        input_dir: str, dir_train: str, dir_test: str
):
    data = pd.read_csv(os.path.join(input_dir, "data.csv"))
    X = data.drop(columns=["target"])
    y = data["target"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    os.makedirs(dir_train, exist_ok=True)
    X_train.to_csv(os.path.join(dir_train, "features.csv"), index=False)
    y_train.to_csv(os.path.join(dir_train, "targets.csv"), index=False)

    os.makedirs(dir_test, exist_ok=True)
    X_test.to_csv(os.path.join(dir_test, "features.csv"), index=False)
    y_test.to_csv(os.path.join(dir_test, "targets.csv"), index=False)


if __name__ == '__main__':
    split()
