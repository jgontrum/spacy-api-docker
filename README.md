# spaCy API Docker

Flask based REST API for spaCy, the great and fast NLP framework.
Supports the English and German language models and returns the analysis structured by sentences and by token.

Please note that currently the dependency trees are not returned.

## Usage

Once started, make a POST request:

```
curl http://localhost:5000/api -d "text:This is a text that I want to be analyzed." -X POST
```

You'll receive a JSON in return:

```
{
  'sentences': LIST_OF_SENTENCES => LIST_OF_TOKENS
  'performance': CALCULATION_TIME_IN_MS,
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

## Start
### Docker
```
docker start -d -p 127.0.0.1:5000:5000 jgontrum/spacyapi:en
```
### Local
```
python server.py
```
