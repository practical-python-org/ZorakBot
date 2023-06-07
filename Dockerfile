FROM python:3.9.16-slim-buster AS builder-image

# install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /src

RUN set -ex \
    # Create a user that will be a shared user between containers
    && addgroup --system --gid 1001 service-user \
    && adduser --system --uid 1001 --gid 1001 --no-create-home zorak-user \

    # Assign ownership of the directory to this user
    && chown -R zorak-user:service-user /src/


WORKDIR /src

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3", "__main__.py"]
USER zorak-user
