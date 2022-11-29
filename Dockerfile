FROM python:3.8-slim-buster

WORKDIR /code

RUN apt-get update
RUN apt-get install -y build-essential

COPY requirements.txt .

RUN pip3 install -r requirements.txt \
    && rm -rf /root/.cache

COPY . .

CMD ["python", "index.py"]