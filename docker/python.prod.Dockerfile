FROM python:3.12

WORKDIR /

RUN python -m pip install --upgrade pip
RUN pip install "poetry==2.1.1"

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

EXPOSE 8000