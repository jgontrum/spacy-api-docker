FROM alpine:3.3

ENV LANG en

RUN mkdir -p /usr/spacyapi
COPY . /usr/spacyapi/

RUN apk add --no-cache python && \
    python -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip install --upgrade pip setuptools && \
    rm -r /root/.cache
RUN apk add --no-cache gcc g++ python-dev openssh ca-certificates
RUN update-ca-certificates

RUN pip install -r /usr/spacyapi/requirements.txt
RUN python -m spacy.${LANG}.download

RUN apk del gcc g++ python-dev

ENTRYPOINT cd /usr/spacyapi && python server.py
