import os
import json

from spacy.cli import download


def download_models():
    languages = os.getenv("languages", "en").split()
    for lang in languages:
        download(model=lang, direct=False)

    print("Updating frontend settings...")
    frontend_settings = json.load(open("frontend/_data.json"))

    frontend_settings['index']['languages'] = {
        l: l for l in languages
    }
    frontend_settings['index']['default_language'] = languages[0]

    json.dump(frontend_settings, open("frontend/_data.json", "w"),
              sort_keys=True,
              indent=2)

    print("Done!")
