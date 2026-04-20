from textual.screen import Screen, ModalScreen
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Header, Footer, ListView, ListItem, Label, ProgressBar, Static, Button, Input
from tui.scripts.element_counter import count_queue_items
from dotenv import set_key

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
        self.total_files = 0

    def compose(self) -> ComposeResult:
        yield Static("Количество файлов которые осталось обработать: 0")
        yield ProgressBar(total=1, show_percentage=True, show_eta=False)

    def on_mount(self) -> None:
        self.total_files = count_queue_items()
        self.update_progress()
        self.set_interval(1, self.update_progress)

    def update_progress(self) -> None:
        remaining = count_queue_items()
        done = max(self.total_files - remaining, 0)

        label = self.query_one("#files-left", Static)
        bar = self.query_one("#files-bar", ProgressBar)

        label.update(f"Количество файлов которые осталось обработать: {remaining}")
        bar.total = max(self.total_files, 1)
        bar.progress = done