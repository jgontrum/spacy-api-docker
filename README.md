# spaCy API Docker

Flask based REST API for spaCy, the great and fast NLP framework.
Supports the English and German language models and returns the analysis structured by sentences and by token.

Please note that currently the dependency trees are not returned.

## Usage

Once started, make a POST request:

```
curl http://localhost:5000/api -d "text=This is a text that I want to be analyzed." -X POST
```

You'll receive a JSON in return:

```
{
  'sentences': [[TOKEN, TOKEN, ...], [TOKEN, TOKEN, ...], ...],
  'performance': CALCULATION_TIME_IN_SEC,
  'version': SPACY_VERSION,
  'numOfSentences': NUM_OF_SENTENCES,
  'numOfTokens': NUM_OF_TOKENS
}
```

```
TOKEN: {
  'token': TOKEN,
  'lemma': LEMMA,
  'tag': TAG,
  'ner': NER,
  'offsets': {
    'begin': BEGIN,
    'end': END
  },
  'oov': OUT_OF_VOCAB,
  'stop': IS_STOPWORD,
  'url': IS_URL,
  'email': IS_MAIL,
  'num': IS_NUM,
  'pos': POS
}
```

## Installation
### Docker
```
docker pull jgontrum/spacyapi:en
or
docker pull jgontrum/spacyapi:de
```
### Local
```
pip install -r requirements.txt

python -m spacy.en.download
or
python -m spacy.de.download
```

## Run
### Docker
```
docker run --name spacyapi -d -p 127.0.0.1:5000:5000 jgontrum/spacyapi:en
```
### Local
```
LANG=en python server.py
or
LANG=de python server.py
```

## Example
### Request
```
curl http://localhost:5000/api -d "text=Das hier ist Peter. Peter ist eine Person." -X POST
```

### Response
```
{
  "performance": 0.0042879581451416016,
  "version": "0.101.0",
  "numOfSentences": 2,
  "numOfTokens": 10,
  "sentences": [
    [
      {
        "offsets": {
          "begin": 0,
          "end": 3
        },
        "oov": false,
        "stop": false,
        "pos": "PRON",
        "tag": "PDS",
        "url": false,
        "lemma": "das",
        "token": "Das",
        "num": false,
        "ner": "",
        "email": false
      },
      {
        "offsets": {
          "begin": 4,
          "end": 8
        },
        "oov": false,
        "stop": false,
        "pos": "ADV",
        "tag": "ADV",
        "url": false,
        "lemma": "hier",
        "token": "hier",
        "num": false,
        "ner": "",
        "email": false
      },
      {
        "offsets": {
          "begin": 9,
          "end": 12
        },
        "oov": false,
        "stop": false,
        "pos": "AUX",
        "tag": "VAFIN",
        "url": false,
        "lemma": "ist",
        "token": "ist",
        "num": false,
        "ner": "",
        "email": false
      },
      {
        "offsets": {
          "begin": 13,
          "end": 18
        },
        "oov": false,
        "stop": false,
        "pos": "PROPN",
        "tag": "NE",
        "url": false,
        "lemma": "peter",
        "token": "Peter",
        "num": false,
        "ner": "PERSON",
        "email": false
      },
      {
        "offsets": {
          "begin": 18,
          "end": 19
        },
        "oov": false,
        "stop": false,
        "pos": "PUNCT",
        "tag": "$.",
        "url": false,
        "lemma": ".",
        "token": ".",
        "num": false,
        "ner": "",
        "email": false
      }
    ],
    [
      {
        "offsets": {
          "begin": 20,
          "end": 25
        },
        "oov": false,
        "stop": false,
        "pos": "PROPN",
        "tag": "NE",
        "url": false,
        "lemma": "peter",
        "token": "Peter",
        "num": false,
        "ner": "PERSON",
        "email": false
      },
      {
        "offsets": {
          "begin": 26,
          "end": 29
        },
        "oov": false,
        "stop": false,
        "pos": "AUX",
        "tag": "VAFIN",
        "url": false,
        "lemma": "ist",
        "token": "ist",
        "num": false,
        "ner": "",
        "email": false
      },
      {
        "offsets": {
          "begin": 30,
          "end": 34
        },
        "oov": false,
        "stop": false,
        "pos": "DET",
        "tag": "ART",
        "url": false,
        "lemma": "eine",
        "token": "eine",
        "num": false,
        "ner": "",
        "email": false
      },
      {
        "offsets": {
          "begin": 35,
          "end": 41
        },
        "oov": false,
        "stop": false,
        "pos": "NOUN",
        "tag": "NN",
        "url": false,
        "lemma": "Person",
        "token": "Person",
        "num": false,
        "ner": "",
        "email": false
      },
      {
        "offsets": {
          "begin": 41,
          "end": 42
        },
        "oov": false,
        "stop": false,
        "pos": "PUNCT",
        "tag": "$.",
        "url": false,
        "lemma": ".",
        "token": ".",
        "num": false,
        "ner": "",
        "email": false
      }
    ]
  ]
}
```
