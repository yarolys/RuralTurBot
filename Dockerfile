FROM python:3.12.7
WORKDIR /RuralTurBot
RUN apk upgrade --update && apk add gcc gcompat musl-dev libffi-dev build-base unixodbc-dev unixodbc --no-cache
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
RUN mkdir -p /app/logs && chmod -R 777 /app/logs
COPY run.py .
COPY alembic.ini .
COPY src ./src
RUN alembic upgrade head
CMD ["python3", "run.py"]
