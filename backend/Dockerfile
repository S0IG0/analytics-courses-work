FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /temp/requirements.txt
COPY ./analytics/ /backend
WORKDIR backend

RUN  pip install --no-cache-dir -r /temp/requirements.txt