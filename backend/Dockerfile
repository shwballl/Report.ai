FROM python:3.11-slim

RUN apt-get update && apt-get install -y git && apt-get clean

WORKDIR /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
