FROM debian:wheezy
MAINTAINER Johannes Gontrum <https://github.com/jgontrum>
ENV LANG en

RUN mkdir -p /usr/spacyapi
COPY . /usr/spacyapi/

RUN apt-get update
RUN apt-get install -y python build-essential gcc g++ python-dev python-setuptools

RUN easy_install pip
RUN pip install --upgrade pip setuptools
RUN pip install -r /usr/spacyapi/requirements.txt

RUN python -m spacy.${LANG}.download

ENTRYPOINT cd /usr/spacyapi && python server.py

EXPOSE 5000
