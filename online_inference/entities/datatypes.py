from pydantic import BaseModel, conlist
from typing import Union, List


class PredictResponse(BaseModel):
    id: int
    target: int


class InputDataRequest(BaseModel):
    data: List[conlist(Union[float, str, None], min_items=14, max_items=14)]  # Batch query
    features: List[str]

