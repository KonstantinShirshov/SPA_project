FROM python:3.13-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE = False

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

RUN mkdir -p /app/media

EXPOSE 8000
