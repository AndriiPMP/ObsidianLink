from textual.screen import Screen, ModalScreen
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, ListView, ListItem, Label, ProgressBar, Static, Button, Input
from tui.scripts.element_counter import count_queue_items
from dotenv import set_key, load_dotenv
from main import main
from threading import Thread
import os
from redis_implement.redis_queue_store import redis_queue_store

class StageScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(
            value="",
            placeholder="Путь к папке",
            id="target-dir",
        )
        yield Button("Сохранить и начать", id="start")
        yield ListView(
            ListItem(Label("0  Полный прогон")),
            id="stage-list",
        )
        yield Footer()

    def on_mount(self):
        self.query_one("#target-dir", Input).focus()

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "start":
            target_dir = self.query_one("#target-dir", Input).value.strip()
            if target_dir:
                self.app.push_screen(ConfirmScreen(target_dir), self.on_confirm)

    def on_confirm(self, confirmed: bool):
        if not confirmed:
            return

        target_dir = self.query_one("#target-dir", Input).value.strip()
        set_key(".env", "TARGET_DIR", target_dir)
        load_dotenv(dotenv_path=".env", override=True)

        self.app.push_screen(ProgressScreen())
        Thread(target=main, daemon=True).start()


class ConfirmScreen(ModalScreen[bool]):
    def __init__(self, target_dir: str) -> None:
        super().__init__()
        self.target_dir = target_dir

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static("Начать обработку?"),
            Button("Да", id="yes"),
            Button("Нет", id="no"),
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)
    

class ProgressScreen(Screen):
    def __init__(self) -> None:
        super().__init__()
        self.total_files = None
        self._progress_started = False

    def compose(self) -> ComposeResult:
        yield Static("Количество файлов которые осталось обработать: 0", id="files-left")
        yield ProgressBar(total=1, show_percentage=True, show_eta=False, id="files-bar")

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