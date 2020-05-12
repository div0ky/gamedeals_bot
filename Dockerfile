FROM python:3.8-slim-buster

MAINTAINER div0ky "me@div0ky.com"

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . ./app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

CMD python div_deals.py