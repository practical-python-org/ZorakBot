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
	CMD [ "python","-u", "build/lib/zorak_bot/__main__.py" ]


