#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "pytest",
#   "textual",
# ]
# ///

from __future__ import annotations

from textual.widgets import Label

from app import DemoApp


async def test_confirm_flow() -> None:
    app = DemoApp()

    async with app.run_test() as pilot:
        await pilot.click('#save')
        await pilot.pause()

        title = pilot.app.query_one('#dialog-title', Label)
        assert title.renderable == 'Save changes?'

        await pilot.click('#confirm')
        await pilot.pause()

        status = pilot.app.query_one('#status', Label)
        assert status.renderable == 'Saved'


async def test_cancel_flow() -> None:
    app = DemoApp()

    async with app.run_test() as pilot:
        await pilot.press('ctrl+s')
        await pilot.pause()
        await pilot.click('#cancel')
        await pilot.pause()

        status = pilot.app.query_one('#status', Label)
        assert status.renderable == 'Cancelled'
