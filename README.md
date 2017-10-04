# spaCy API Docker

**Ready-to-use Docker images for the [spaCy NLP library](https://github.com/explosion/spaCy).**

Try the demo for [spaCy 1.9.0](https://spacy.jgontrum.com/ui/?text=This%20is%20an%20example.&model=en_core_web_sm&cpu=0&cph=0) or [spaCy 2.0.0 (alpha)](https://spacy2.jgontrum.com/ui/?text=This%20is%20an%20example.&model=en_core_web_sm&cpu=0&cph=0)!

### Features
- Use the awesome spaCy NLP framwork with other programming languages.
- Better scaling: One NLP - multiple services.
- Build using the official [spaCy REST services](https://github.com/explosion/spacy-services).
- Dependency parsing visualisation with [displaCy](https://demos.explosion.ai/displacy/).
- Docker images for **English**, **German**, **Spanish** and **French**.
- Automated builds to stay up to date with spaCy.
- Used spaCy version: 1.9.0 / 2.0.0alpha.

Please note that this is a completely new API and is incompatible with the previous one. If you still need them, use `jgontrum/spacyapi:en-legacy` or  `jgontrum/spacyapi:de-legacy`.

*Documentation, API- and frontend code based upon [spaCy REST services](https://github.com/explosion/spacy-services) by [Explosion AI](https://explosion.ai).*

---

## Images

| Image                    | Description                                | Build |
|--------------------------|--------------------------------------------|--------|
| jgontrum/spacyapi:base   | Base image, containing no language model   | ![Build Status](https://travis-ci.org/jgontrum/spacy-api-docker.svg?branch=master) |
| jgontrum/spacyapi:latest | English language model                     | ![Build Status](https://travis-ci.org/jgontrum/spacy-api-docker.svg?branch=master) |
| jgontrum/spacyapi:en     | English language model                     | ![Build Status](https://travis-ci.org/jgontrum/spacy-api-docker.svg?branch=master) |
| jgontrum/spacyapi:de     | German language model                      | ![Build Status](https://travis-ci.org/jgontrum/spacy-api-docker.svg?branch=master) |
| jgontrum/spacyapi:es     | Spanish language model                     | ![Build Status](https://travis-ci.org/jgontrum/spacy-api-docker.svg?branch=master) |
| jgontrum/spacyapi:fr     | French language model                      | ![Build Status](https://travis-ci.org/jgontrum/spacy-api-docker.svg?branch=master) |
| jgontrum/spacyapi:all    | Contains EN, DE, ES and FR language models | ![Build Status](https://travis-ci.org/jgontrum/spacy-api-docker.svg?branch=master) |
| jgontrum/spacyapi:base_v2   | Base image for spaCy 2.0  | ![Build Status](https://travis-ci.org/jgontrum/spacy-api-docker.svg?branch=spacy2) |
| jgontrum/spacyapi:en_v2     | English language model for spaCy 2.0                    | ![Build Status](https://travis-ci.org/jgontrum/spacy-api-docker.svg?branch=spacy2) |
| jgontrum/spacyapi:de_v2     | German language model for spaCy 2.0                    | ![Build Status](https://travis-ci.org/jgontrum/spacy-api-docker.svg?branch=spacy2) |
| jgontrum/spacyapi:es_v2     | Spanish language model for spaCy 2.0                    | ![Build Status](https://travis-ci.org/jgontrum/spacy-api-docker.svg?branch=spacy2) |
| jgontrum/spacyapi:all_v2    | Contains EN, DE and FR language models for spaCy 2.0 | ![Build Status](https://travis-ci.org/jgontrum/spacy-api-docker.svg?branch=spacy2) |
| jgontrum/spacyapi:en-legacy | Old API with English model | *legacy* |
| jgontrum/spacyapi:de-legacy | Old API with German model | *legacy* |

---

## Usage

`docker run -p "127.0.0.1:8080:80" jgontrum/spacyapi:en`

All models are loaded at start up time. Depending on the model size and server 
performance, this can take a few minutes.


The displaCy frontend is available at `/ui`.

### Docker Compose
```json
version: '2'

services:
  spacyapi:
    image: jgontrum/spacyapi:en
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
    "model":"en",
    "collapse_punctuation": 0,
    "collapse_phrases": 1
}
```

| Name | Type | Description |
| --- | --- | --- |
| `text` | string | text to be parsed |
| `model` | string | identifier string for a model installed on the server |
| `collapse_punctuation` | boolean | Merge punctuation onto the preceding token? |
| `collapse_phrases` | boolean | Merge noun chunks and named entities into single tokens? |  


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

| Name | Type | Description |
| --- | --- | --- |
| `arcs` | array | data to generate the arrows |
| `dir` | string | direction of arrow (`"left"` or `"right"`) |
| `start` | integer | offset of word the arrow starts **on** |
| `end` | integer | offset of word the arrow ends **on** |
| `label` | string | dependency label |
| `words` | array | data to generate the words |
| `tag` | string | part-of-speech tag |
| `text` | string | token |

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

### `POST` `/ent/`

Example request:

```json
{
    "text": "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously.",
    "model": "en"
}
```

| Name | Type | Description |
| --- | --- | --- |
| `text` | string | text to be parsed |
| `model` | string | identifier string for a model installed on the server  |

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
    { "end": 20, "start": 5,  "type": "PERSON" },
    { "end": 67, "start": 61, "type": "ORG" },
    { "end": 75, "start": 71, "type": "DATE" }
]
```

| Name | Type | Description |
| --- | --- | --- |
| `end` | integer | character offset the entity ends **after** |
| `start` | integer | character offset the entity starts **on** |
| `type` | string | entity type |



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

| Name | Type | Description |
| --- | --- | --- |
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


