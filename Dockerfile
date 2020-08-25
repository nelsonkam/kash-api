FROM python:3.7-alpine
RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev git wget bash \
  && apk add postgresql-dev \
  && apk add libffi-dev py-cffi

RUN apk add --no-cache tzdata
ENV TZ Europe/London

RUN pip install poetry

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY poetry.lock pyproject.toml /usr/src/app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY ./ /usr/src/app
RUN chmod +x docker-entrypoint.sh

ENV FLASK_APP app.py
