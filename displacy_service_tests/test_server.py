import falcon.testing
import json

from displacy_service.server import APP


class TestAPI(falcon.testing.TestCase):
    def setUp(self):
        super(TestAPI, self).setUp()
        self.app = APP

    def test_deps(self):
        result = self.simulate_post(
            path='/dep',
            body='''{"text": "This is a test.", "model": "en",
                 "collapse_punctuation": false,
                 "collapse_phrases": false}'''
        )
        result = json.loads(result.text)
        words = [w['text'] for w in result['words']]
        assert words == ["This", "is", "a", "test", "."]

    def test_ents(self):
        result = self.simulate_post(
            path='/ent',
            body='''{"text": "What a great company Google is.",
                    "model": "en"}''')
        ents = json.loads(result.text)
        assert ents == [
            {"start": 21, "end": 27, "type": "ORG", "text": "Google"}]

    def test_tag_full(self):
        toks = self.simulate_post(
            path='/tag',
            json={
                "text": "Foo",
                "model": "en",
            }).json
        assert toks[0] == {'start': 0, 'end': 3, 'text': 'Foo', 'orth' : 'Foo', 'lemma': 'foo', 'pos': 'PROPN', 'tag': 'NNP',
                           'dep': 'ROOT', 'ent_type': '', 'ent_iob': 'O', 'norm': 'foo',
                           'lower': 'foo', 'shape': 'Xxx', 'prefix': 'F', 'suffix': 'Foo', 'is_alpha': True,
                           'is_ascii': True, 'is_digit': False, 'is_lower': False, 'is_upper': False, 'is_title': True,
                           'is_punct': False, 'is_left_punct': False, 'is_right_punct': False, 'is_space': False,
                           'is_bracket': False, 'is_quote': False, 'is_currency': False, 'like_url': False,
                           'like_num': False, 'like_email': False, 'is_oov': True, 'is_stop': False, 'cluster': 0}

    def test_tag_with_filter(self):
        toks = self.simulate_post(
            path='/tag',
            json={
                "text": "Fed raises interest rates 0.5 percent.",
                "model": "en",
                "attr_filter": ["text", "start", "end", "lemma", "pos"]
            }).json

        assert toks == [{'start': 0, 'end': 3, 'text': 'Fed', 'lemma': 'fed', 'pos': 'PROPN'},
                        {'start': 4, 'end': 10, 'text': 'raises', 'lemma': 'raise', 'pos': 'VERB'},
                        {'start': 11, 'end': 19, 'text': 'interest', 'lemma': 'interest', 'pos': 'NOUN'},
                        {'start': 20, 'end': 25, 'text': 'rates', 'lemma': 'rate', 'pos': 'NOUN'},
                        {'start': 26, 'end': 29, 'text': '0.5', 'lemma': '0.5', 'pos': 'NUM'},
                        {'start': 30, 'end': 37, 'text': 'percent', 'lemma': 'percent', 'pos': 'NOUN'},
                        {'start': 37, 'end': 38, 'text': '.', 'lemma': '.', 'pos': 'PUNCT'}]

    def test_tag_with_sents(self):
        sents = self.simulate_post(
            path='/tag',
            json={
                "text": "This a test that should split into sentences! This is the second.",
                "model": "en",
                "include_sentences": True,
                "attr_filter": ["text", "start", "end", "lemma", "pos"]
            }).json
        assert sents == [
            {'text': 'This a test that should split into sentences!',
             'start': 0,
             'end': 45,
             'tokens': [
                 {'text': 'This', 'start': 0, 'end': 4, 'lemma': 'this', 'pos': 'DET'},
                 {'text': 'a', 'start': 5, 'end': 6, 'lemma': 'a', 'pos': 'DET'},
                 {'text': 'test', 'start': 7, 'end': 11, 'lemma': 'test', 'pos': 'NOUN'},
                 {'text': 'that', 'start': 12, 'end': 16, 'lemma': 'that', 'pos': 'ADJ'},
                 {'text': 'should', 'start': 17, 'end': 23, 'lemma': 'should', 'pos': 'VERB'},
                 {'text': 'split', 'start': 24, 'end': 29, 'lemma': 'split', 'pos': 'VERB'},
                 {'text': 'into', 'start': 30, 'end': 34, 'lemma': 'into', 'pos': 'ADP'},
                 {'text': 'sentences', 'start': 35, 'end': 44, 'lemma': 'sentence', 'pos': 'NOUN'},
                 {'text': '!', 'start': 44, 'end': 45, 'lemma': '!', 'pos': 'PUNCT'}
             ]},
            {
                'text': 'This is the second.',
                'start': 46,
                'end': 65,
                'tokens': [
                    {'text': 'This', 'start': 46, 'end': 50, 'lemma': 'this', 'pos': 'DET'},
                    {'text': 'is', 'start': 51, 'end': 53, 'lemma': 'be', 'pos': 'VERB'},
                    {'text': 'the', 'start': 54, 'end': 57, 'lemma': 'the', 'pos': 'DET'},
                    {'text': 'second', 'start': 58, 'end': 64, 'lemma': 'second', 'pos': 'ADJ'},
                    {'text': '.', 'start': 64, 'end': 65, 'lemma': '.', 'pos': 'PUNCT'}
                ]}
        ]

    def test_sents(self):
        sentences = self.simulate_post(
            path='/sents',
            json={
                "text": """This a test that should split into sentences!
                This is the second. Is this the third?""",
                "model": "en"
            }
        )
        assert sentences.json == ['This a test that should split into sentences!',
                             'This is the second.', 'Is this the third?']
