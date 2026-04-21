#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "httpx",
#   "pydantic",
# ]
# ///

from __future__ import annotations

import asyncio

import httpx
from pydantic import BaseModel, Field


class TodoCreate(BaseModel):
    title: str
    done: bool = False


class Todo(BaseModel):
    id: str = Field(alias='_id')
    title: str
    done: bool = False


class CrudCrudAPI:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self.client = client

    async def create_todo(self, payload: TodoCreate) -> Todo:
        response = await self.client.post('/todos', json=payload.model_dump())
        response.raise_for_status()
        return Todo.model_validate(response.json())

    async def get_todo(self, todo_id: str) -> Todo:
        response = await self.client.get(f'/todos/{todo_id}')
        response.raise_for_status()
        return Todo.model_validate(response.json())


def handler(request: httpx.Request) -> httpx.Response:
    assert request.headers['X-Trace'] == 'test-run'
    assert request.url.host == 'crudcrud.com'

    if request.method == 'POST' and request.url.path == '/api/demo-token/todos':
        assert request.content == b'{"title":"write tests","done":false}'
        return httpx.Response(
            201,
            json={'_id': 'todo-42', 'title': 'write tests', 'done': False},
        )

    if request.method == 'GET' and request.url.path == '/api/demo-token/todos/todo-42':
        return httpx.Response(
            200,
            json={'_id': 'todo-42', 'title': 'write tests', 'done': False},
        )

    return httpx.Response(404, json={'detail': 'not found'})


async def main() -> None:
    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(
        base_url='https://crudcrud.com/api/demo-token',
        headers={'X-Trace': 'test-run'},
        transport=transport,
    ) as client:
        api = CrudCrudAPI(client)
        created = await api.create_todo(TodoCreate(title='write tests'))
        fetched = await api.get_todo(created.id)
        assert fetched.id == 'todo-42'
        assert fetched.title == 'write tests'
        print('crudcrud transport test passed')


if __name__ == '__main__':
    asyncio.run(main())
