FROM python:3.9

RUN mkdir -p /app
WORKDIR /app

RUN pip install "poetry==1.4.1"
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

ADD src /app/src
ADD mapping /app/src/mapping

EXPOSE 8080

CMD gunicorn --chdir src "fdk_reports_bff:create_app()"  --config=src/fdk_reports_bff/gunicorn_config.py
