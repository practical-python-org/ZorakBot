FROM python:3.9.12-buster
WORKDIR /code
COPY . /code
RUN pip3 install --upgrade pip
RUN pip3 install py-cord beautifulsoup4 requests matplotlib DateTime pytz pistonapi
EXPOSE 5000
ENTRYPOINT ["python3", "zorak_bot/__main__.py", "-dt", "MTAyMjI0MDg1OTU2OTI3ODk5Nw.Guk5B8.6FdyKRV00RWAbosAyDOBacvv9UksGvUowcBpBE"], 
#CMD ["token", ""]