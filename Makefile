.PHONY: clean start generate_typescript docker

all: dashboardapi.egg-info

dashboardapi.egg-info:
	poetry install
	poetry run pre-commit install
	poetry run configure_gitlab 2> /dev/null
	echo "Python is installed in: `poetry run which python`"

clean:
	rm -rfv bin develop-eggs dist downloads eggs env parts .cache .scannerwork
	rm -fv .DS_Store .coverage .installed.cfg bootstrap.py .coverage
	find . -name '*.pyc' -exec rm -fv {} \;
	find . -name '*.pyo' -exec rm -fv {} \;
	find . -depth -name '*.egg-info' -exec rm -rfv {} \;
	find . -depth -name '__pycache__' -exec rm -rfv {} \;
	poetry env remove `poetry run which python`

start: dashboardapi.egg-info
	doppler run -- poetry run api

generate_typescript: dashboardapi.egg-info
	poetry run generate_ts_models

docker:
	docker build -t dashboardapi .
