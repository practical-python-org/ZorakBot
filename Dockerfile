FROM python:3.11.4-slim-buster AS builder-image
ENV PYTHONUNBUFFERED=1

COPY . /code
WORKDIR /code

RUN pip install . && apt-get update && apt-get install -y ffmpeg

ENTRYPOINT ["zorak"]
