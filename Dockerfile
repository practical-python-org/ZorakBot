FROM python:3.9.16-slim-buster AS builder-image
ENV PYTHONUNBUFFERED=1

COPY . /code
WORKDIR /code

CMD pip install .
# make sure all messages always reach console

ENTRYPOINT ["zorak"]
