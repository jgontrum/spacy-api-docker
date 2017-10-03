import pytest

import spacy
from displacy_service.parse import Parse


@pytest.fixture(scope="session")
def nlp():
    return spacy.load('en')


def test_parse_to_json(nlp):
    parse = Parse(nlp, u'Hello, this is a parse.', False, False)
    json_model = parse.to_json()
    assert len(json_model['words']) == 7
    assert len(json_model['arcs']) == 6


def test_collapse_punct(nlp):
    parse = Parse(nlp, u'Hello, this is a parse.', True, False)
    json_model = parse.to_json()
    assert len(json_model['words']) == 5
    assert len(json_model['arcs']) == 4
    assert [w['text'] for w in json_model['words']] == [u'Hello,', u'this', u'is', u'a', u'parse.']
    

def test_collapse_phrases(nlp):
    parse = Parse(nlp, u'This example is a parse.', False, True)
    json_model = parse.to_json()
    assert len(json_model['words']) == 4
    assert len(json_model['arcs']) == 3
    assert [w['text'] for w in json_model['words']] == [u'This example', u'is', u'a parse', u'.']
