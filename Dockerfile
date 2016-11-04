FROM debian:jessie
MAINTAINER Johannes Gontrum <https://github.com/jgontrum>
ENV LANG en
ENV PORT 5000

RUN mkdir -p /usr/spacyapi
COPY . /usr/spacyapi/

RUN apt-get update
RUN apt-get install -y python build-essential gcc g++ python-dev python-setuptools python-pip
RUN export PIP_CERT=`python -m pip._vendor.requests.certs`

RUN pip install --upgrade pip setuptools
RUN pip install -r /usr/spacyapi/requirements.txt

RUN python -m spacy.${LANG}.download parser

ENTRYPOINT cd /usr/spacyapi && python server.py

EXPOSE PORT
