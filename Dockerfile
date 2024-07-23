FROM python:3.11-slim-buster
RUN apt-get update &&  apt-get install -y git

COPY . .

COPY requirements.txt .

RUN pip install -r requirements.txt

ENV IS_CONTAINER=True

EXPOSE 8050

CMD ["python", "index.py"]




