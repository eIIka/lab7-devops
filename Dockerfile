# Модель: Модель балки Ейлера-Бернуллі (5 семестр)
# Автор: Калкатін Владислав, група АІ-235

FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir numpy matplotlib flask

COPY main.py .

EXPOSE 5000

CMD ["python", "main.py"]