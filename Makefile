.PHONY: clean start test poetry

PYTHON3=python3.8

all: env/bin/python

poetry:
	curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

requirements.txt:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

env/bin/python:
	$(PYTHON3) -m venv env
	env/bin/pip install --upgrade pip
	env/bin/pip install wheel
	env/bin/pip install -r requirements.txt
	env/bin/python setup.py develop

clean:
	rm -rfv bin develop-eggs dist downloads eggs env parts .cache .scannerwork
	rm -fv .DS_Store .coverage .installed.cfg bootstrap.py .coverage
	find . -name '*.pyc' -exec rm -fv {} \;
	find . -name '*.pyo' -exec rm -fv {} \;
	find . -depth -name '*.egg-info' -exec rm -rfv {} \;
	find . -depth -name '__pycache__' -exec rm -rfv {} \;
	rm requirements.txt

test: env/bin/python
	languages=en env/bin/download_models
	env/bin/py.test displacy_service_tests

start: env/bin/python
	env/bin/run_server
