from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .handlers import info
from .utils import settings


# Create the service and hide the documentation if it is deployed in production
app = FastAPI(title=settings.name, version=settings.version)

# Configure CORS
if settings.allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Define the router
app.include_router(info.router)


def start():
    import uvicorn

    uvicorn.run("spacy_service.service:app", host="127.0.0.1", port=8800, reload=True)
