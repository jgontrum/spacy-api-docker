import falcon.testing
import json

from displacy_service.server import APP


class TestAPI(falcon.testing.TestCase):
    def __init__(self):
        self.api = APP


def test_deps():
    test_api = TestAPI()
    result = test_api.simulate_post(path='/dep',
                body='''{"text": "This is a test.", "model": "en",
                         "collapse_punctuation": false, 
                         "collapse_phrases": false}''')
    result = json.loads(result.text)
    words = [w['text'] for w in result['words']]
    assert words == ["This", "is", "a", "test", "."]


def test_ents():
    test_api = TestAPI()
    result = test_api.simulate_post(path='/ent',
                body='''{"text": "What a great company Google is.",
                "model": "en"}''')
    ents = json.loads(result.text)
    assert ents == [
        {"start": 21, "end": 27, "type": "ORG", "text": "Google"}]
