FROM python:3.12.4-slim-bullseye AS builder-image

ENV PYTHONUNBUFFERED=1

WORKDIR /code

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY setup.py /code/setup.py
COPY setup.cfg /code/setup.cfg
COPY versioneer.py /code/versioneer.py
COPY pyproject.toml /code/pyproject.toml
COPY Resources/ /code/Resources
COPY README.md /code/README.md
COPY src /code/src

RUN pip uninstall -y zorak && \
    pip install .

ENTRYPOINT ["zorak"]
