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
    assert sentence_parse == [{'sentence': 'This a test that should split into sentences!',
                               'dep_parse':
                                   {'words': [{'text': 'This', 'tag': 'DT'},
                                              {'text': 'a', 'tag': 'DT'},
                                              {'text': 'test', 'tag': 'NN'},
                                              {'text': 'that', 'tag': 'WDT'},
                                              {'text': 'should', 'tag': 'MD'},
                                              {'text': 'split', 'tag': 'VB'},
                                              {'text': 'into', 'tag': 'IN'},
                                              {'text': 'sentences', 'tag': 'NNS'},
                                              {'text': '!', 'tag': '.'}],
                                    'arcs': [{'start': 0, 'end': 2, 'label': 'det', 'text': 'This', 'dir': 'left'},
                                             {'start': 1, 'end': 2, 'label': 'det', 'text': 'a', 'dir': 'left'},
                                             {'start': 3, 'end': 5, 'label': 'nsubj', 'text': 'that', 'dir': 'left'},
                                             {'start': 4, 'end': 5, 'label': 'aux', 'text': 'should', 'dir': 'left'},
                                             {'start': 2, 'end': 5, 'label': 'relcl', 'text': 'split', 'dir': 'right'},
                                             {'start': 5, 'end': 6, 'label': 'prep', 'text': 'into', 'dir': 'right'},
                                             {'start': 6, 'end': 7, 'label': 'pobj', 'text': 'sentences', 'dir': 'right'},
                                             {'start': 2, 'end': 8, 'label': 'punct', 'text': '!', 'dir': 'right'}]}},
                              {'sentence': 'This is the second.',
                               'dep_parse': {'words':
                                                 [{'text': 'This', 'tag': 'DT'},
                                                  {'text': 'is', 'tag': 'VBZ'},
                                                  {'text': 'the', 'tag': 'DT'},
                                                  {'text': 'second', 'tag': 'JJ'},
                                                  {'text': '.', 'tag': '.'}],
                                             'arcs': [{'start': 0, 'end': 1, 'label': 'nsubj', 'text': 'This', 'dir': 'left'},
                                                      {'start': 2, 'end': 3, 'label': 'det', 'text': 'the', 'dir': 'left'},
                                                      {'start': 1, 'end': 3, 'label': 'attr', 'text': 'second', 'dir': 'right'},
                                                      {'start': 1, 'end': 4, 'label': 'punct', 'text': '.', 'dir': 'right'}]}},
                              {'sentence': 'Is this the third?',
                               'dep_parse': {'words':
                                                 [{'text': 'Is', 'tag': 'VBZ'},
                                                  {'text': 'this', 'tag': 'DT'},
                                                  {'text': 'the', 'tag': 'DT'},
                                                  {'text': 'third', 'tag': 'JJ'},
                                                  {'text': '?', 'tag': '.'}],
                                             'arcs': [{'start': 0, 'end': 1, 'label': 'nsubj', 'text': 'this', 'dir': 'right'},
                                                      {'start': 2, 'end': 3, 'label': 'det', 'text': 'the', 'dir': 'left'},
                                                      {'start': 0, 'end': 3, 'label': 'attr', 'text': 'third', 'dir': 'right'},
                                                      {'start': 0, 'end': 4, 'label': 'punct', 'text': '?', 'dir': 'right'}]}}]