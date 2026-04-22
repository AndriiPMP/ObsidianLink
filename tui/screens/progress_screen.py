from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import ProgressBar, Static, Button
from tui.scripts.element_counter import count_queue_items
import os
from redis_implement.redis_queue_store import redis_queue_store
from screens.option_screen import OptionScreen

class ProgressScreen(Screen):

    def __init__(self) -> None:
        super().__init__()
        self.total_files = None
        self._progress_started = False
        self._option_button_shown = False

    def compose(self) -> ComposeResult:
        yield Static("Количество файлов которые осталось обработать: 0", id="files-left")
        yield ProgressBar(total=1, show_percentage=True, show_eta=False, id="files-bar")
        yield Button("Перейти к выбору", id="to-option", disabled=True)

    def on_mount(self) -> None:
        self.set_interval(0.5, self.wait_for_queue_file)

    def wait_for_queue_file(self) -> None:
        if self._progress_started:
            return

        if not os.path.exists(redis_queue_store):
            return
        
        total = count_queue_items()
        if total is None:
            return
        
        self.total_files = total
        self._progress_started = True
        self.update_progress()
        self.set_interval(1, self.update_progress)

    def update_progress(self) -> None:
        remaining = count_queue_items()

        if remaining is None or self.total_files is None:
            return
    
        done = max(self.total_files - remaining, 0)

        label = self.query_one("#files-left", Static)
        bar = self.query_one("#files-bar", ProgressBar)

        label.update(f"Количество файлов которые осталось обработать: {remaining}")
        bar.update(total=max(self.total_files, 1), progress=done)

        if done >= self.total_files and not self._option_button_shown:
            self._option_button_shown = True
            self.mount(Button("Завершить и вернуться", id="to-option"))

    def on_button_pressed(self, event: Button.Pressed) -> None:
            if event.button.id == "to-option":
                self.app.push_screen(OptionScreen())