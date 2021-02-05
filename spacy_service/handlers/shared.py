import spacy

from ..utils import settings

nlp = spacy.load(settings.spacy_model)
