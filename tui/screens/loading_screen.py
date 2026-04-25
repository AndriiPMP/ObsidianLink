from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import LoadingIndicator
from script.assembled.assembled_sort_files import task_done
from screens.option_screen import OptionScreen
from threading import Thread


class LoadingScreen(Screen):
    def compose(self) -> ComposeResult:
        yield LoadingIndicator()

    def on_mount(self) -> None:
        task_done.clear()
        Thread(target=self._wait_done, daemon=True).start()

    def _wait_done(self) -> None:
        task_done.wait()
        self.app.call_from_thread(self.app.switch_screen, OptionScreen())