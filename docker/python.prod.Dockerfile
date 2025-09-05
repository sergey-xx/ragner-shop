FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install "poetry==2.1.4"

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main

COPY . .

EXPOSE 8000