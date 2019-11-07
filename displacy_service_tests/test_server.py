import falcon.testing
import json

from displacy_service.server import APP


class TestAPI(falcon.testing.TestCase):
    def __init__(self):
        self.api = APP


def test_deps():
    test_api = TestAPI()
    result = test_api.simulate_post(
        path='/dep',
        body='''{"text": "This is a test.", "model": "en",
             "collapse_punctuation": false,
             "collapse_phrases": false}'''
    )
    result = json.loads(result.text)
    words = [w['text'] for w in result['words']]
    assert words == ["This", "is", "a", "test", "."]


def test_ents():
    test_api = TestAPI()
    result = test_api.simulate_post(
        path='/ent',
        body='''{"text": "What a great company Google is.",
                "model": "en"}''')
    ents = json.loads(result.text)
    assert ents == [
        {"start": 21, "end": 27, "type": "ORG", "text": "Google"}]


def test_sents():
    test_api = TestAPI()
    sentences = test_api.simulate_post(
        path='/sent',
        body='''{"text": "This a test that should split into sentences!
        This is the second. Is this the third?", "model": "en"}'''
    )

    assert sentences == ['This a test that should split into sentences!',
                         'This is the second.', 'Is this the third?']


def test_sents_dep():
    test_api = TestAPI()
    sentence_parse = test_api.simulate_post(
        path='/sents_dep',
        body='''{"text": "This a test that should split into sentences!
        This is the second. Is this the third?", "model": "en",
        "collapse_punctuation": false, "collapse_phrases": false}'''
    )
    sentences = [sp["sentence"] for sp in sentence_parse]
    assert sentences == [
        "This a test that should split into sentences!",
        "This is the second.",
        "Is this the third?",
    ]
    words = [[w["text"] for w in sp["dep_parse"]["words"]] for sp in sentence_parse]
    assert words == [
        ["This", "a", "test", "that", "should", "split", "into", "sentences", "!"],
        ["This", "is", "the", "second", "."],
        ["Is", "this", "the", "third", "?"],
    ]
