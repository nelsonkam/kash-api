FROM python:3.7-alpine
RUN apk update \
  && apk add --virtual build-deps curl gcc python3-dev musl-dev git wget bash make g++ \
  && apk add postgresql-dev \
  && apk add libffi-dev py-cffi \
  && apk add jpeg-dev zlib-dev libjpeg \
  && apk add --update py-pip

ENV DJANGO_SETTINGS_MODULE app_main.settings
ENV CRYPTOGRAPHY_DONT_BUILD_RUST 1

RUN apk add --no-cache tzdata
ENV TZ Europe/London

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ../../requirements.txt /usr/src/app/

RUN pip install -r requirements.txt


COPY ../../ /usr/src/app
