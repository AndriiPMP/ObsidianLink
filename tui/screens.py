from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label, ProgressBar, Static
from tui.scripts.element_counter import count_queue_items

class StageScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header()
        yield ListView(
            ListItem(Label("0  Полный прогон")),
            ListItem(Label("1  Начать с этапа 2")),
            id="stage-list",
        )
        yield Footer()

    def on_mount(self):
        self.query_one(ListView).focus()

    def on_list_view_selected(self, event: ListView.Selected):
        self.dismiss(event.index)


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