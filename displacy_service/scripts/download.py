import os

from spacy.cli import download


def download_models():
    for lang in os.getenv("languages", "en").split():
        download(model=lang, direct=False)
