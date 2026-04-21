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
import os

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


async def main() -> None:
    endpoint = os.getenv('CRUDCRUD_ENDPOINT')
    if not endpoint:
        raise SystemExit(
            'Set CRUDCRUD_ENDPOINT to something like '
            'https://crudcrud.com/api/<token>'
        )

    async with httpx.AsyncClient(
        base_url=endpoint,
        timeout=httpx.Timeout(10.0, connect=3.0),
        headers={'User-Agent': 'myapp/1.0'},
    ) as client:
        api = CrudCrudAPI(client)
        created = await api.create_todo(TodoCreate(title='review httpx skill'))
        fetched = await api.get_todo(created.id)
        print(fetched.model_dump_json(indent=2, by_alias=True))


if __name__ == '__main__':
    asyncio.run(main())
