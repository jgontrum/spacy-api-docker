.PHONY: clean english german

all: english

english: env
	python -m spacy.en.download parser

german: env
	python -m spacy.de.download parser

env:
	virtualenv env -p python3.5 --no-site-packages
	env/bin/pip install --upgrade pip
	env/bin/pip install wheel

clean:
	rm -rfv develop-eggs dist downloads eggs env parts 
	rm -fv .DS_Store .coverage .installed.cfg
	find . -name '*.pyc' -exec rm -fv {} \; 
	find . -name '*.pyo' -exec rm -fv {} \; 
	find . -depth -name '*.egg-info' -exec rm -rfv {} \; 
	find . -depth -name '__pycache__' -exec rm -rfv {} \;
