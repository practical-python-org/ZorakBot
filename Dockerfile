FROM python:3.11.4-slim-buster AS builder-image

# install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /src
WORKDIR /src

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3", "__main__.py"]
