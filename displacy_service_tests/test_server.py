import falcon.testing
import pytest
import json

from displacy_service.server import APP, MODELS


model = MODELS[0]


@pytest.fixture()
def api():
    return falcon.testing.TestClient(APP)


def test_deps(api):
    result = api.simulate_post(
        path='/dep',
        body='{{"text": "This is a test.", "model": "{model}", "collapse_punctuation": false, "collapse_phrases": false}}'.format(model=model)
    )
    result = json.loads(result.text)
    words = [w['text'] for w in result['words']]
    assert words == ["This", "is", "a", "test", "."]


def test_ents(api):
    result = api.simulate_post(
        path='/ent',
        body='{{"text": "What a great company Google is.", "model": "{model}"}}'.format(model=model))
    ents = json.loads(result.text)
    assert ents == [
        {"start": 21, "end": 27, "type": "ORG", "text": "Google"}]


def test_sents(api):
    sentences = api.simulate_post(
        path='/sents',
        body='{{"text": "This a test that should split into sentences! This is the second. Is this the third?", "model": "{model}"}}'.format(model=model)
    )

    assert sentences.json == ['This a test that should split into sentences!', 'This is the second.', 'Is this the third?']


def test_sents_dep(api):
    sentence_parse = api.simulate_post(
        path='/sents_dep',
        body='{{"text": "This a test that should split into sentences! This is the second. Is this the third?", "model": "{model}", "collapse_punctuation": false, "collapse_phrases": false}}'.format(model=model)
    )
    sentences = [sp["sentence"] for sp in sentence_parse.json]
    assert sentences == [
        "This a test that should split into sentences!",
        "This is the second.",
        "Is this the third?",
    ]
    words = [[w["text"] for w in sp["dep_parse"]["words"]] for sp in sentence_parse.json]
    assert words == [
        ["This", "a", "test", "that", "should", "split", "into", "sentences", "!"],
        ["This", "is", "the", "second", "."],
        ["Is", "this", "the", "third", "?"],
    ]

    arcs = [[arc for arc in sp['dep_parse']['arcs']] for sp in sentence_parse.json]
    assert arcs == [[{'start': 0, 'end': 2, 'label': 'det', 'text': 'This', 'dir': 'left'},
                     {'start': 1, 'end': 2, 'label': 'det', 'text': 'a', 'dir': 'left'},
                     {'start': 2, 'end': 2, 'label': 'ROOT', 'text': 'test', 'dir': 'root'},
                     {'start': 3, 'end': 5, 'label': 'nsubj', 'text': 'that', 'dir': 'left'},
                     {'start': 4, 'end': 5, 'label': 'aux', 'text': 'should', 'dir': 'left'},
                     {'start': 2, 'end': 5, 'label': 'relcl', 'text': 'split', 'dir': 'right'},
                     {'start': 5, 'end': 6, 'label': 'prep', 'text': 'into', 'dir': 'right'},
                     {'start': 6, 'end': 7, 'label': 'pobj', 'text': 'sentences', 'dir': 'right'},
                     {'start': 2, 'end': 8, 'label': 'punct', 'text': '!', 'dir': 'right'}],
                    [{'start': 9, 'end': 10, 'label': 'nsubj', 'text': 'This', 'dir': 'left'},
                     {'start': 10, 'end': 10, 'label': 'ROOT', 'text': 'is', 'dir': 'root'},
                     {'start': 11, 'end': 12, 'label': 'det', 'text': 'the', 'dir': 'left'},
                     {'start': 10, 'end': 12, 'label': 'attr', 'text': 'second', 'dir': 'right'},
                     {'start': 10, 'end': 13, 'label': 'punct', 'text': '.', 'dir': 'right'}],
                    [{'start': 14, 'end': 14, 'label': 'ROOT', 'text': 'Is', 'dir': 'root'},
                     {'start': 14, 'end': 15, 'label': 'nsubj', 'text': 'this', 'dir': 'right'},
                     {'start': 16, 'end': 17, 'label': 'det', 'text': 'the', 'dir': 'left'},
                     {'start': 14, 'end': 17, 'label': 'attr', 'text': 'third', 'dir': 'right'},
                     {'start': 14, 'end': 18, 'label': 'punct', 'text': '?', 'dir': 'right'}]]

@pytest.mark.parametrize('endpoint, expected_message', [
    ('/dep', 'Dependency parsing failed'),
    ('/ent', 'Text parsing failed'),
    ('/sents', 'Sentence tokenization failed'),
    ('/sents_dep', 'Sentence tokenization and Dependency parsing failed'),
])
def test_bad_model_error_handling(endpoint, expected_message, api):
    response = api.simulate_post(
        path=endpoint,
        body='{"text": "Here is some text for testing.", "model": "fake_model"}'
    )
    assert expected_message == response.json['title']
    assert "Can't find model 'fake_model'." in response.json["description"]
