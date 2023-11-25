FROM python:3.9-buster
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8050

ENV IS_CONTAINER=True

CMD ["python3", "./index.py"]

