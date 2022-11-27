# TECHOPARK | MLOps | HW2

## Quick start
Build docker image from inside the `./online_inference/` directory:
```commandline
docker build -t mlops_ml_model .
```

Or pool a docker image from docker-hub:
```commandline
docker pull riardenmetal/mlops_ml_model:v2
```

## Quick run
- Run docker container :
   ```commandline
   docker run -p 8000:8000  riardenmetal/mlops_ml_model:v2
   ```
 - Go to http://127.0.0.1:8000/model to see if the model is ready.

## Make requests
From inside the `./online_inference/` directory:
```commandline
python3 request.py
```

## Quick test
From inside the `./online_inference/` directory:
```commandline
python3 -m unittest 
```

## Docker Optimization
Предположим мы изменили логику нашего сервера -> нам нужно повторно собрать докер образ:
1. [v1](https://hub.docker.com/layers/riardenmetal/mlops_ml_model/v1/images/sha256-f5e41fc83ca0dba682e29784606cacee92331bc658543296869817265171fb56?context=explore) Изначальный сценарий :
   - rebuild time ~ 53s
2. [v2](https://hub.docker.com/layers/riardenmetal/mlops_ml_model/v2/images/sha256-b27fdafb676294b62c242051be0d0b215d3f1a980988ce11b4837767ec6a3f5a?context=explore) С оптимизацией кеширования слоев:
   - rebuild time ~ 0,457s
