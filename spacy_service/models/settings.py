from typing import Optional, List, Literal

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


class Settings(BaseSettings):
    name: str = "spaCy Service API"
    target: str = "local"
    version: str = "dev"

    allowed_origins: List[str] = []

    logging_level: Literal["critical", "error", "warning", "info", "debug"] = "info"
    sentry: Optional[str] = None
    spacy_model: str = "en_core_web_sm"
