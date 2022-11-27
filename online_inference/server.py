import sys
import os
import uvicorn
from fastapi import FastAPI
import logging
from entities.model_funcs import *

app = FastAPI()
model = None

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.on_event("startup") # Инициализируем пайплан, хранящийся на сервере
def loading_model():
    global model
    model_path = os.getenv("PATH_TO_MODEL")
    if model_path is None:
        err = "PATH_TO_MODEL was not specified"
        logger.error(err)
        raise RuntimeError(err)
    model = load_model(model_path)
    logger.info(f"Loaded model from {model_path}")


@app.get("/")
def root():
    return "Model online inference"


@app.get("/model")
def check_model():
    return "[ERROR]: Model not initialized" if model is None else "[OK]: Model initialized"

@app.get("/predict/", response_model=List[PredictResponse])
def predict(request: InputDataRequest):
    return make_predict(request, model)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
