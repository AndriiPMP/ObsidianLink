from textual.app import App, ComposeResult
from textual.widgets import LoadingIndicator

class LoadingScreen(App):
    def compose(self) -> ComposeResult:
        yield LoadingIndicator()