.PHONY: clean start build-and-push test

PYTHON3=python3.6

all: env/bin/python

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

test: env/bin/python
	languages=en env/bin/download_models
	env/bin/py.test displacy_service_tests

start: env/bin/python
	env/bin/run_server
