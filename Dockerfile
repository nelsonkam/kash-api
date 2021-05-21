FROM python:3.7-alpine
RUN apk update \
  && apk add --virtual build-deps curl gcc python3-dev musl-dev git wget bash make g++ \
  && apk add postgresql-dev \
  && apk add libffi-dev py-cffi \
  && apk add jpeg-dev zlib-dev libjpeg \
  && apk add --update py-pip

ENV DJANGO_SETTINGS_MODULE kash_api.settings
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

RUN apk add --no-cache tzdata
ENV TZ Europe/London

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY poetry.lock pyproject.toml /usr/src/app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY ./ /usr/src/app
RUN chmod +x docker-entrypoint.sh
