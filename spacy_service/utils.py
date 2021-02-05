import logging
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG

from .models.settings import Settings

settings = Settings()


# Initialize sentry if it is configured
if settings.sentry:
    import sentry_sdk

    print("Initialize Sentry...")
    sentry_sdk.init(settings.sentry)

# Configure the logger
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s | %(name)s | %(levelname)s : %(message)s")

ch.setFormatter(formatter)
logger = logging.getLogger("spacy_service")
logger.addHandler(ch)
logger.setLevel(
    {
        "critical": CRITICAL,
        "error": ERROR,
        "warning": WARNING,
        "info": INFO,
        "debug": DEBUG,
    }.get(settings.logging_level, INFO)
)


class LoggerMixin:
    @property
    def logger(self) -> logging.Logger:
        return logging.getLogger(f"spacy_service.{type(self).__name__}")
