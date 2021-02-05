from typing import List, Dict

from . import Model


class Token(Model):
    text: str
    token: str
    pos: str
    lemma: str
    ner: str

    is_stop_word: bool

    character_offset: int
    offset: int
    length: int

    morphology: Dict[str, str] = {}


class Sentence(Model):
    sentence: str
    tokens: List[Token]
    num_tokens: int


class TextAnalysis(Model):
    text: str
    sentences: List[Sentence]
    num_sentences: int


class SpacyResponse(Model):
    num_texts: int
    texts: List[TextAnalysis]
