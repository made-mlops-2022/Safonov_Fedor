FROM python:3.8

WORKDIR /app

COPY . .

ENV PATH_TO_MODEL=models/model.pkl
RUN pip install -r requirements.txt  # Запускается, когда строим образ

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]  # Каждый раз при запуске образа