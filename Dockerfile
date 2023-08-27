FROM python:3.9.16-slim-buster AS builder-image
ENV PYTHONUNBUFFERED=1

COPY . /code
WORKDIR /code

RUN pip install .

ENTRYPOINT ["zorak"]
