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

### Running Tests

In order to run unit tests locally `pytest` is included.

`docker run -it jgontrum/spacyapi:en_v2 app/env/bin/pytest app/displacy_service_tests`

### Special Cases

The API includes rudimentary support for specifying [special cases](https://spacy.io/usage/linguistic-features#special-cases)
for your deployment. Currently only basic special cases are supported; for example, in the spaCy parlance:

```python
tokenizer.add_special_case("isn't", [{ORTH: "isn't"}])
```

They can be supplied in an environment variable corresponding to the desired language model. For example, `en_special_cases`
or `en_core_web_lg_special_cases`. They are configured as a single comma-delimited string, such as `"isn't,doesn't,won't"`.

Use the following syntax to specify basic special case rules, such as for preserving contractions:

`docker run -p "127.0.0.1:8080:80" -e en_special_cases="isn't,doesn't" jgontrum/spacyapi:en_v2`

You can also configure this in a `.env` file if using `docker-compose` as above.

---

## REST API Documentation

### `GET` `/ui/`

displaCy frontend is available here.

---

### `POST` `/dep`

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

### `POST` `/ent`

Example request:

```json
{
  "text": "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously.",
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

url = "http://localhost:8000/ent"
message_text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."
headers = {'content-type': 'application/json'}
d = {'text': message_text, 'model': 'en'}

response = requests.post(url, data=json.dumps(d), headers=headers)
r = response.json()
```

Example response:

```json
[
  { "end": 20, "start": 5, "type": "PERSON" },
  { "end": 67, "start": 61, "type": "ORG" },
  { "end": 75, "start": 71, "type": "DATE" }
]
```

| Name    | Type    | Description                                |
| ------- | ------- | ------------------------------------------ |
| `end`   | integer | character offset the entity ends **after** |
| `start` | integer | character offset the entity starts **on**  |
| `type`  | string  | entity type                                |

```
curl -s localhost:8000/ent -d '{"text":"Pastafarians are smarter than people with Coca Cola bottles.", "model":"en"}'
```

```json
[
  {
    "end": 12,
    "start": 0,
    "type": "NORP"
  },
  {
    "end": 51,
    "start": 42,
    "type": "ORG"
  }
]
```

---

### `POST` `/sents`

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

---

### `POST` `/sents_dep`

Combination of `/sents` and `/dep`, returns sentences and dependency parses

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

url = "http://localhost:8000/sents_dep"
message_text = "In 2012 I was a mediocre developer. But today I am at least a bit better."
headers = {'content-type': 'application/json'}
d = {'text': message_text, 'model': 'en'}

response = requests.post(url, data=json.dumps(d), headers=headers)
r = response.json()
```

Example response:

```json
[
  {
    "sentence": "In 2012 I was a mediocre developer.",
    "dep_parse": {
      "arcs": [
        {
          "dir": "left",
          "end": 3,
          "label": "prep",
          "start": 0,
          "text": "In"
        },
        {
          "dir": "right",
          "end": 1,
          "label": "pobj",
          "start": 0,
          "text": "2012"
        },
        {
          "dir": "left",
          "end": 3,
          "label": "nsubj",
          "start": 2,
          "text": "I"
        },
        {
          "dir": "left",
          "end": 6,
          "label": "det",
          "start": 4,
          "text": "a"
        },
        {
          "dir": "left",
          "end": 6,
          "label": "amod",
          "start": 5,
          "text": "mediocre"
        },
        {
          "dir": "right",
          "end": 6,
          "label": "attr",
          "start": 3,
          "text": "developer"
        },
        {
          "dir": "right",
          "end": 7,
          "label": "punct",
          "start": 3,
          "text": "."
        }
      ],
      "words": [
        {
          "tag": "IN",
          "text": "In"
        },
        {
          "tag": "CD",
          "text": "2012"
        },
        {
          "tag": "PRP",
          "text": "I"
        },
        {
          "tag": "VBD",
          "text": "was"
        },
        {
          "tag": "DT",
          "text": "a"
        },
        {
          "tag": "JJ",
          "text": "mediocre"
        },
        {
          "tag": "NN",
          "text": "developer"
        },
        {
          "tag": ".",
          "text": "."
        }
      ]
    }
  },
  {
    "sentence": "But today I am at least a bit better.",
    "dep_parse": {
      "arcs": [
        {
          "dir": "left",
          "end": 11,
          "label": "cc",
          "start": 8,
          "text": "But"
        },
        {
          "dir": "left",
          "end": 11,
          "label": "npadvmod",
          "start": 9,
          "text": "today"
        },
        {
          "dir": "left",
          "end": 11,
          "label": "nsubj",
          "start": 10,
          "text": "I"
        },
        {
          "dir": "left",
          "end": 13,
          "label": "advmod",
          "start": 12,
          "text": "at"
        },
        {
          "dir": "left",
          "end": 15,
          "label": "advmod",
          "start": 13,
          "text": "least"
        },
        {
          "dir": "left",
          "end": 15,
          "label": "det",
          "start": 14,
          "text": "a"
        },
        {
          "dir": "left",
          "end": 16,
          "label": "npadvmod",
          "start": 15,
          "text": "bit"
        },
        {
          "dir": "right",
          "end": 16,
          "label": "acomp",
          "start": 11,
          "text": "better"
        },
        {
          "dir": "right",
          "end": 17,
          "label": "punct",
          "start": 11,
          "text": "."
        }
      ],
      "words": [
        {
          "tag": "CC",
          "text": "But"
        },
        {
          "tag": "NN",
          "text": "today"
        },
        {
          "tag": "PRP",
          "text": "I"
        },
        {
          "tag": "VBP",
          "text": "am"
        },
        {
          "tag": "IN",
          "text": "at"
        },
        {
          "tag": "JJS",
          "text": "least"
        },
        {
          "tag": "DT",
          "text": "a"
        },
        {
          "tag": "NN",
          "text": "bit"
        },
        {
          "tag": "RBR",
          "text": "better"
        },
        {
          "tag": ".",
          "text": "."
        }
      ]
    }
  }
]
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

### `GET` `/{model}/schema`

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
