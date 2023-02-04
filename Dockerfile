FROM python:3.9.12-buster
COPY . .
RUN pip3 install --upgrade pip
RUN pip3 install py-cord beautifulsoup4 requests matplotlib DateTime pytz pistonapi toml feedparser html2text pymongo
EXPOSE 5000
ENTRYPOINT ["python3", "zorak_bot/__main__.py", "-dt", "DISCORDTOKEN"]
#CMD ["token", ""]
