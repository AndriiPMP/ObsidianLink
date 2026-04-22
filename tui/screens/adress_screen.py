from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label, Button, Input
from dotenv import set_key, load_dotenv
from main import main
from threading import Thread
from tui.screens.progress_screen import ProgressScreen
from tui.screens.approve_screen import ConfirmScreen

class AdressScreen(Screen):

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