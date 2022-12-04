import click
import pandas as pd
import os
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

@click.command()
@click.option("--dir_train")
@click.option("--dir_save")
def train(dir_train: str, dir_save: str):
    X_train = pd.read_csv(os.path.join(dir_train, "features.csv"))
    y_train = pd.read_csv(os.path.join(dir_train, "targets.csv"))

    pipeline  = Pipeline([('normalize', StandardScaler()), ('clf', LogisticRegression())])
    pipeline.fit(X_train, y_train)

    os.makedirs(dir_save, exist_ok=True)
    with open(os.path.join(dir_save, "model.pickle"), "wb") as f:
        pickle.dump(pipeline, f)




if __name__ == '__main__':
    train()
