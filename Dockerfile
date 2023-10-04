FROM python:3.12.0-slim-bullseye AS builder-image

ENV PYTHONUNBUFFERED=1

COPY . /code
WORKDIR /code

RUN pip install . && apt-get update && apt-get install -y ffmpeg

ENTRYPOINT ["zorak"]
