FROM python:3.12.4-alpine
WORKDIR /RuralTurBot
RUN apk upgrade --update && apk add gcc gcompat musl-dev libffi-dev build-base unixodbc-dev unixodbc --no-cache
COPY pyproject.toml .
COPY poetry.lock .
RUN pip install poetry 
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
