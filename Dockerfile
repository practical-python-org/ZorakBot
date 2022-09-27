FROM python:3.9.12-buster

	WORKDIR /code
	RUN echo \
	   && apt-get update \
	   && apt-get --yes install apt-file \
	   && apt-file update
	RUN echo \
	   && apt-get --yes install build-essential
	RUN apt-get install ffmpeg libsm6 libxext6  -y
	RUN pip3 install --upgrade pip
	COPY . /code
	RUN pip3 --no-cache-dir install .
   EXPOSE 5000
	CMD [ "python3","-u", "build/lib/zorak_bot/__main__.py","-dt", "TOKEN","-ll","40","--log-file","./logs/logs.txt", "--err-file", "./logs/errors.txt", "--flask-host", "0.0.0.0", "--flask-port", "80"]


