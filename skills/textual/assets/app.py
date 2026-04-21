#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "textual",
# ]
# ///

from __future__ import annotations

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Input, Label


class ConfirmScreen(ModalScreen[bool]):
    def compose(self) -> ComposeResult:
        yield Label('Save changes?', id='dialog-title')
        yield Button('Cancel', id='cancel')
        yield Button('Confirm', id='confirm', classes='primary')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(event.button.id == 'confirm')


class DemoApp(App[None]):
    CSS_PATH = 'app.tcss'
    BINDINGS = [
        Binding('ctrl+s', 'open_confirm', 'Save'),
        Binding('q', 'quit', 'Quit'),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder='Type something', id='name')
        yield Button('Save', id='save')
        yield Label('Idle', id='status')
        yield Footer()

    def action_open_confirm(self) -> None:
        self.push_screen(ConfirmScreen(), self._on_confirm)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'save':
            self.action_open_confirm()

    def _on_confirm(self, confirmed: bool) -> None:
        status = self.query_one('#status', Label)
        status.update('Saved' if confirmed else 'Cancelled')


if __name__ == '__main__':
    DemoApp().run()
