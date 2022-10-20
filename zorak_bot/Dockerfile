FROM python:3.9.12-buster
	WORKDIR /code
	RUN mkdir /cogs
	COPY main.py .
	COPY /cogs/ ./cogs
	RUN pip3 install --upgrade pip
	RUN pip3 install py-cord beautifulsoup4 requests matplotlib DateTime pytz

ENTRYPOINT ["python3", "main.py"]
CMD ["token", ""]