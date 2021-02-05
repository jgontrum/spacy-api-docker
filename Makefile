.PHONY: clean start

all: spacy_service.egg-info

spacy_service.egg-info:
	poetry install
	poetry run pre-commit install
	echo "Python is installed in: `poetry run which python`"

clean:
	rm -rfv bin develop-eggs dist downloads eggs env parts .cache .scannerwork
	rm -fv .DS_Store .coverage .installed.cfg bootstrap.py .coverage
	find . -name '*.pyc' -exec rm -fv {} \;
	find . -name '*.pyo' -exec rm -fv {} \;
	find . -depth -name '*.egg-info' -exec rm -rfv {} \;
	find . -depth -name '__pycache__' -exec rm -rfv {} \;
	poetry env remove `poetry run which python`

start: spacy_service.egg-info
	doppler run -- poetry run api
