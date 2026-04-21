#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "fastapi",
#   "jinja2",
#   "uvicorn",
# ]
# ///

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).parent
TEMPLATES = Jinja2Templates(directory=str(BASE_DIR / 'templates'))

app = FastAPI()
app.mount('/static', StaticFiles(directory=BASE_DIR / 'static'), name='static')


PROJECTS = [
    {'id': 1, 'name': 'Atlas', 'status': 'active', 'description': 'Customer portal refresh'},
    {'id': 2, 'name': 'Beacon', 'status': 'paused', 'description': 'Internal reporting pipeline'},
    {'id': 3, 'name': 'Comet', 'status': 'done', 'description': 'Inventory sync migration'},
]


@app.get('/projects', response_class=HTMLResponse)
async def projects_page(request: Request) -> HTMLResponse:
    return TEMPLATES.TemplateResponse(
        request=request,
        name='page/projects.jinja',
        context={
            'page_title': 'Projects',
            'projects': PROJECTS,
        },
    )


@app.get('/projects/partial', response_class=HTMLResponse)
async def projects_partial(request: Request) -> HTMLResponse:
    return TEMPLATES.TemplateResponse(
        request=request,
        name='partials/project_list.jinja',
        context={
            'projects': PROJECTS,
        },
    )
