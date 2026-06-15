"""FastAPI application entrypoint.

Keeps HTTP wiring thin so business logic stays testable outside
of the web framework. Routes validate at the boundary and delegate
to plain functions.
"""

from __future__ import annotations

from fastapi import FastAPI

from myapp import __version__
from myapp.routes import router


def create_app() -> FastAPI:
    """Build and configure the FastAPI application.

    A factory keeps tests isolated: each test builds a fresh app
    instead of sharing mutable module state.
    """
    app = FastAPI(title='myapp', version=__version__)
    app.include_router(router)
    return app


# Module-level instance for `fastapi run src/myapp/main.py` (see docker/Dockerfile).
app = create_app()
