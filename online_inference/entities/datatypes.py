from pydantic import BaseModel, conlist, root_validator, validator
from typing import Union, List


class PredictResponse(BaseModel):
    id: int
    target: int

    @validator("target")
    def prediction_is_binary(cls, val):
        if val not in [0, 1]:
            raise ValueError("prediction must be binary [0, 1]")
        return val


class InputDataRequest(BaseModel):
    data: List[conlist(Union[float, str, None], min_items=14, max_items=14)]  # Batch query
    features: List[str]

    @validator("data")
    def not_empty(cls, val):
        if len(val) == 0:
            raise ValueError("There should be at least one row of data")
        return val

    @validator("data")
    def same_size_rows(cls, val):
        base_len = len(val[0])
        for elem in val:
            if len(elem) != base_len:
                raise ValueError("All rows should be same size")
        return val

    @root_validator
    def same_size_data_features(cls, vals):
        if len(vals["features"]) != len(vals["data"][0]):
            raise ValueError("Features and data should be same size")
        return vals
