from fastapi import APIRouter

from ..utils import settings

router = APIRouter()


@router.get("/version")
def version() -> str:
    return settings.version


@router.get("/health")
def healthcheck() -> str:
    return "green"
