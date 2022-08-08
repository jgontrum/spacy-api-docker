import os

from spacy.cli import download


def download_models():
    languages = os.getenv("languages", "en").split()
    for lang in languages:
        download(model=lang, direct=False)

    print("Done!")


if __name__ == "__main__":
    download_models()
