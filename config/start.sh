#! /usr/bin/env sh
set -e

DEFAULT_APP_MODULE=displacy_service.scripts.app
export APP_MODULE=${APP_MODULE:-$DEFAULT_APP_MODULE}

DEFAULT_GUNICORN_CONF=/app/config/gunicorn_conf.py
export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}

# Start Gunicorn
exec gunicorn -c "$GUNICORN_CONF" "$APP_MODULE"
