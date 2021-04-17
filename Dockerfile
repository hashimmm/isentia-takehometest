FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y --no-install-recommends postgresql-client libpq-dev \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt \
    && rm /requirements.txt

COPY ./src /code
