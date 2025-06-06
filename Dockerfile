FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y gcc build-essential libssl-dev default-libmysqlclient-dev && \
    apt-get clean

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
