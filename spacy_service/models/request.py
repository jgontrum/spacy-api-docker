from typing import List

from . import Model


class SpacyRequest(Model):
    texts: List[str]
