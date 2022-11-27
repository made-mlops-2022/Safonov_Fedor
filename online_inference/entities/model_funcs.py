from .datatypes import *
from sklearn.pipeline import Pipeline
import pandas as pd
from fastapi import HTTPException
import pickle


def make_predict(input_request: InputDataRequest, model: Pipeline,) -> List[PredictResponse]:
    x_input = input_request.data
    features = input_request.features

    if len(x_input) == 0:
        raise HTTPException(
            status_code=400, detail="Query is empty"
        )

    data = pd.DataFrame(x_input, columns=features)
    ids = [x for x in data['id']]
    data = data.drop(['id'], axis=1)
    predicts = model.predict(data)
    result = [
        PredictResponse(id=data_id, target=int(condition)) for data_id, condition in zip(ids, predicts)
    ]
    return result


def load_model(model_path: str) -> Pipeline:
    model = pickle.load(open(model_path, 'rb'))
    return model