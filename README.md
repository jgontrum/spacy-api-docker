# spaCy API Docker

**Ready-to-use Docker images for the [spaCy NLP library](https://github.com/explosion/spaCy).**

### Features

- Use the awesome spaCy NLP framework with other programming languages.
- Better scaling: One NLP - multiple services.
- Build using the official [spaCy REST services](https://github.com/explosion/spacy-services).
- Dependency parsing visualisation with [displaCy](https://demos.explosion.ai/displacy/).
- Docker images for **English**, **German**, **Spanish**, **Italian**, **Dutch** and **French**.
- Automated builds to stay up to date with spaCy.
- Current spaCy version: 2.0.16

Please note that this is a completely new API and is incompatible with the previous one. If you still need them, use `jgontrum/spacyapi:en-legacy` or `jgontrum/spacyapi:de-legacy`.

_Documentation, API- and frontend code based upon [spaCy REST services](https://github.com/explosion/spacy-services) by [Explosion AI](https://explosion.ai)._

---

## Images

| Image                       | Description                                                       |
| --------------------------- | ----------------------------------------------------------------- |
| jgontrum/spacyapi:base_v2   | Base image for spaCy 2.0, containing no language model            |
| jgontrum/spacyapi:en_v2     | English language model, spaCy 2.0                                 |
| jgontrum/spacyapi:de_v2     | German language model, spaCy 2.0                                  |
| jgontrum/spacyapi:es_v2     | Spanish language model, spaCy 2.0                                 |
| jgontrum/spacyapi:fr_v2     | French language model, spaCy 2.0                                  |
| jgontrum/spacyapi:pt_v2     | Portuguese language model, spaCy 2.0                              |
| jgontrum/spacyapi:it_v2     | Italian language model, spaCy 2.0                                 |
| jgontrum/spacyapi:nl_v2     | Dutch language model, spaCy 2.0                                   |
| jgontrum/spacyapi:all_v2    | Contains EN, DE, ES, PT, NL, IT and FR language models, spaCy 2.0 |
| _OLD RELEASES_              |                                                                   |
| jgontrum/spacyapi:base      | Base image, containing no language model                          |
| jgontrum/spacyapi:latest    | English language model                                            |
| jgontrum/spacyapi:en        | English language model                                            |
| jgontrum/spacyapi:de        | German language model                                             |
| jgontrum/spacyapi:es        | Spanish language model                                            |
| jgontrum/spacyapi:fr        | French language model                                             |
| jgontrum/spacyapi:all       | Contains EN, DE, ES and FR language models                        |
| jgontrum/spacyapi:en-legacy | Old API with English model                                        |
| jgontrum/spacyapi:de-legacy | Old API with German model                                         |

---

## Usage

`docker run -p "127.0.0.1:8080:80" jgontrum/spacyapi:en_v2`

All models are loaded at start up time. Depending on the model size and server
performance, this can take a few minutes.

The displaCy frontend is available at `/ui`.

### Docker Compose

```json
version: '2'

services:
  spacyapi:
    image: jgontrum/spacyapi:en_v2
    ports:
      - "127.0.0.1:8080:80"
    restart: always

```

---

## REST API Documentation

### `GET` `/ui/`

displaCy frontend is available here.

---

### `POST` `/dep/`

Example request:

```json
{
  "text": "They ate the pizza with anchovies",
  "model": "en",
  "collapse_punctuation": 0,
  "collapse_phrases": 1
}
```

| Name                   | Type    | Description                                              |
| ---------------------- | ------- | -------------------------------------------------------- |
| `text`                 | string  | text to be parsed                                        |
| `model`                | string  | identifier string for a model installed on the server    |
| `collapse_punctuation` | boolean | Merge punctuation onto the preceding token?              |
| `collapse_phrases`     | boolean | Merge noun chunks and named entities into single tokens? |

Example request using the Python [Requests library](http://docs.python-requests.org/en/master/):

```python
import json
import requests

url = "http://localhost:8000/dep"
message_text = "They ate the pizza with anchovies"
headers = {'content-type': 'application/json'}
d = {'text': message_text, 'model': 'en'}

response = requests.post(url, data=json.dumps(d), headers=headers)
r = response.json()
```

Example response:

```json
{
  "arcs": [
    { "dir": "left", "start": 0, "end": 1, "label": "nsubj" },
    { "dir": "right", "start": 1, "end": 2, "label": "dobj" },
    { "dir": "right", "start": 1, "end": 3, "label": "prep" },
    { "dir": "right", "start": 3, "end": 4, "label": "pobj" },
    { "dir": "left", "start": 2, "end": 3, "label": "prep" }
  ],
  "words": [
    { "tag": "PRP", "text": "They" },
    { "tag": "VBD", "text": "ate" },
    { "tag": "NN", "text": "the pizza" },
    { "tag": "IN", "text": "with" },
    { "tag": "NNS", "text": "anchovies" }
  ]
}
```

| Name    | Type    | Description                                |
| ------- | ------- | ------------------------------------------ |
| `arcs`  | array   | data to generate the arrows                |
| `dir`   | string  | direction of arrow (`"left"` or `"right"`) |
| `start` | integer | offset of word the arrow starts **on**     |
| `end`   | integer | offset of word the arrow ends **on**       |
| `label` | string  | dependency label                           |
| `words` | array   | data to generate the words                 |
| `tag`   | string  | part-of-speech tag                         |
| `text`  | string  | token                                      |

---

Curl command:

```
curl -s localhost:8000/dep -d '{"text":"Pastafarians are smarter than people with Coca Cola bottles.", "model":"en"}'
```

```json
{
  "arcs": [
    {
      "dir": "left",
      "end": 1,
      "label": "nsubj",
      "start": 0
    },
    {
      "dir": "right",
      "end": 2,
      "label": "acomp",
      "start": 1
    },
    {
      "dir": "right",
      "end": 3,
      "label": "prep",
      "start": 2
    },
    {
      "dir": "right",
      "end": 4,
      "label": "pobj",
      "start": 3
    },
    {
      "dir": "right",
      "end": 5,
      "label": "prep",
      "start": 4
    },
    {
      "dir": "right",
      "end": 6,
      "label": "pobj",
      "start": 5
    }
  ],
  "words": [
    {
      "tag": "NNPS",
      "text": "Pastafarians"
    },
    {
      "tag": "VBP",
      "text": "are"
    },
    {
      "tag": "JJR",
      "text": "smarter"
    },
    {
      "tag": "IN",
      "text": "than"
    },
    {
      "tag": "NNS",
      "text": "people"
    },
    {
      "tag": "IN",
      "text": "with"
    },
    {
      "tag": "NNS",
      "text": "Coca Cola bottles."
    }
  ]
}
```

---

### `POST` `/tag/`

Example request:

```json
{
  "text": "Fed raises interest rates 0.5 percent.",
  "model": "en"
  "include_sentences": false,
  "attr_filter": ["text", "start", "end", "lemma", "pos"]
}
```

| Name                | Type    | Description                                           |
| ------------------- | ------- | ----------------------------------------------------- |
| `text`              | string  | text to be parsed                                     |
| `model`             | string  | identifier string for a model installed on the server |
| `include_sentences` | boolean | include sentence layer                                |
| `attr_filter`       | array   | array of token attributes to include in response      |

Example request using the Python [Requests library](http://docs.python-requests.org/en/master/):

```python
import json
import requests

url = "http://localhost:8000/ent"
message_text = "Fed raises interest rates 0.5 percent."
headers = {'content-type': 'application/json'}
d = {'text': message_text, 'model': 'en', 'include_sentences': False, "attr_filter": ['text', 'start', 'end', 'lemma', 'pos']}

response = requests.post(url, data=json.dumps(d), headers=headers)
r = response.json()
```

Example response:

```json
[
{"start": 0, "end": 3, "text": "Fed", "lemma": "fed", "pos": "PROPN"},
{"start": 4, "end": 10, "text": "raises", "lemma": "raise", "pos": "VERB"},
{"start": 11, "end": 19, "text": "interest", "lemma": "interest", "pos": "NOUN"},
{"start": 20, "end": 25, "text": "rates", "lemma": "rate", "pos": "NOUN"},
{"start": 26, "end": 29, "text": "0.5", "lemma": "0.5", "pos": "NUM"},
{"start": 30, "end": 37, "text": "percent", "lemma": "percent", "pos": "NOUN"},
{"start": 37, "end": 38, "text": ".", "lemma": ".", "pos": "PUNCT"}
]
```

| Name             | Type    | Description                               |
| ---------------- | ------- | ----------------------------------------- |
| `end`            | integer | character offset the token ends **after** |
| `start`          | integer | character offset the token starts **on**  |
| `text`           | string  |                                           |
| `orth`           | string  |                                           |
| `lemma`          | string  |                                           |
| `pos`            | string  |                                           |
| `tag`            | string  |                                           |
| `dep`            | string  |                                           |
| `text`           | string  |                                           |
| `ent_type`       | string  |                                           |
| `ent_iob`        | string  |                                           |
| `norm`           | string  |                                           |
| `lower`          | string  |                                           |
| `shape`          | string  |                                           |
| `prefix`         | string  |                                           |
| `suffix`         | string  |                                           |
| `is_alpha`       | string  |                                           |
| `is_ascii`       | string  |                                           |
| `is_digit`       | string  |                                           |
| `is_lower`       | string  |                                           |
| `is_upper`       | string  |                                           |
| `is_title`       | string  |                                           |
| `is_punct`       | string  |                                           |
| `is_left_punct`  | string  |                                           |
| `is_right_punct` | string  |                                           |
| `is_space`       | string  |                                           |
| `is_bracket`     | string  |                                           |
| `is_currency`    | string  |                                           |
| `like_url`       | string  |                                           |
| `like_num`       | string  |                                           |
| `like_email`     | string  |                                           |
| `is_oov`         | string  |                                           |
| `is_stop`        | string  |                                           |
| `cluster`        | string  |                                           |

```
curl -s localhost:8000/tag -d '{"text":"This a test that should split into sentences! This is the second.", "model":"en", "include_sentences": true, "attr_filter": ["text", "start", "end", "lemma", "pos"]}'
```

```json
[
{"text": "This a test that should split into sentences!",
 "start": 0,
 "end": 45,
 "tokens": [
     {"text": "This", "start": 0, "end": 4, "lemma": "this", "pos": "DET"},
     {"text": "a", "start": 5, "end": 6, "lemma": "a", "pos": "DET"},
     {"text": "test", "start": 7, "end": 11, "lemma": "test", "pos": "NOUN"},
     {"text": "that", "start": 12, "end": 16, "lemma": "that", "pos": "ADJ"},
     {"text": "should", "start": 17, "end": 23, "lemma": "should", "pos": "VERB"},
     {"text": "split", "start": 24, "end": 29, "lemma": "split", "pos": "VERB"},
     {"text": "into", "start": 30, "end": 34, "lemma": "into", "pos": "ADP"},
     {"text": "sentences", "start": 35, "end": 44, "lemma": "sentence", "pos": "NOUN"},
     {"text": "!", "start": 44, "end": 45, "lemma": "!", "pos": "PUNCT"}
 ]},
{
    "text": "This is the second.",
    "start": 46,
    "end": 65,
    "tokens": [
        {"text": "This", "start": 46, "end": 50, "lemma": "this", "pos": "DET"},
        {"text": "is", "start": 51, "end": 53, "lemma": "be", "pos": "VERB"},
        {"text": "the", "start": 54, "end": 57, "lemma": "the", "pos": "DET"},
        {"text": "second", "start": 58, "end": 64, "lemma": "second", "pos": "ADJ"},
        {"text": ".", "start": 64, "end": 65, "lemma": ".", "pos": "PUNCT"}
    ]}
]
```

---

### `POST` `/sents/`

Example request:

```json
{
  "text": "In 2012 I was a mediocre developer. But today I am at least a bit better.",
  "model": "en"
}
```

| Name    | Type   | Description                                           |
| ------- | ------ | ----------------------------------------------------- |
| `text`  | string | text to be parsed                                     |
| `model` | string | identifier string for a model installed on the server |

Example request using the Python [Requests library](http://docs.python-requests.org/en/master/):

```python
import json
import requests

url = "http://localhost:8000/sents"
message_text = "In 2012 I was a mediocre developer. But today I am at least a bit better."
headers = {'content-type': 'application/json'}
d = {'text': message_text, 'model': 'en'}

response = requests.post(url, data=json.dumps(d), headers=headers)
r = response.json()
```

Example response:

```json
["In 2012 I was a mediocre developer.", "But today I am at least a bit better."]
```

### `GET` `/models`

List the names of models installed on the server.

Example request:

```
GET /models
```

Example response:

```json
["en", "de"]
```

---

### `GET` `/{model}/schema/`

Example request:

```
GET /en/schema
```

| Name    | Type   | Description                                           |
| ------- | ------ | ----------------------------------------------------- |
| `model` | string | identifier string for a model installed on the server |

Example response:

```json
{
  "dep_types": ["ROOT", "nsubj"],
  "ent_types": ["PERSON", "LOC", "ORG"],
  "pos_types": ["NN", "VBZ", "SP"]
}
```

---

### `GET` `/version`

Show the used spaCy version.

Example request:

```
GET /version
```

Example response:

```json
{
  "spacy": "1.9.0"
}
```
