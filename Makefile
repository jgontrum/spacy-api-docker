.PHONY: clean english german run-de run-en

all: english

english: env/lib/python3.5/site-packages/spacy/data/en-1.1.0

german: env/lib/python3.5/site-packages/spacy/data/de-1.0.0

env/lib/python3.5/site-packages/spacy/data/en-1.1.0: env
	env/bin/python -m spacy.en.download parser

env/lib/python3.5/site-packages/spacy/data/de-1.0.0: env
	env/bin/python -m spacy.de.download parser

run-de:
	LANG=de env/bin/python server.py

run-en:
	LANG=en env/bin/python server.py

env:
	virtualenv env -p python3.5 --no-site-packages
	env/bin/pip install --upgrade pip
	env/bin/pip install wheel
	env/bin/pip install -r requirements.txt

clean:
	rm -rfv develop-eggs dist downloads eggs env parts 
	rm -fv .DS_Store .coverage .installed.cfg
	find . -name '*.pyc' -exec rm -fv {} \; 
	find . -name '*.pyo' -exec rm -fv {} \; 
	find . -depth -name '*.egg-info' -exec rm -rfv {} \; 
	find . -depth -name '__pycache__' -exec rm -rfv {} \;
