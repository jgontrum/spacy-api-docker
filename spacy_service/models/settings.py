from enum import Enum
from logging import NOTSET, CRITICAL, ERROR, WARNING, INFO, DEBUG
from typing import Optional, List

import requests
from pydantic import BaseSettings
from os import environ as env

if env.get("DOPPLER_TOKEN"):
    env_vars = requests.get(
        "https://api.doppler.com/v3/configs/config/secrets/download?format=json",
        headers={"Content-Type": "application/json", "api-key": env["DOPPLER_TOKEN"]},
    ).json()
    for key, value in env_vars.items():
        env[key] = value


class LogLevel(int, Enum):
    critical = CRITICAL
    error = ERROR
    warning = WARNING
    info = INFO
    debug = DEBUG
    notset = NOTSET


class Settings(BaseSettings):
    name: str = "spaCy Service API"
    target: str = "local"
    version: str = "dev"

    allowed_origins: List[str] = []

    logging_level: LogLevel = LogLevel.info
    sentry: Optional[str] = None
