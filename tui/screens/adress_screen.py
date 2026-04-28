from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import Header, Footer, Button, Input, Static
from dotenv import set_key, load_dotenv
from script.assembled.assembled_create_links import create_links
from script.assembled.assembled_sort_files import sort_files
from threading import Thread
from tui.screens.approve_screen import ConfirmScreen

class AdressScreen(Screen):

    def __init__(self, action: str) -> None:
        self.action = action
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(
            value="",
            placeholder="Путь к папке",
            id="target-dir",
        )
        
        if self.action == "sort":
            yield Input(
                value="",
                placeholder="Путь к файлам",
                id="sort-dir",
            )
        yield Static("", id="error-text")    
        yield Button("Сохранить и начать", id="start")
        yield Footer()

    def on_mount(self):
        
        self.query_one("#target-dir", Input).focus()

    def on_button_pressed(self, event: Button.Pressed):

        if event.button.id != "start":
            return
        
        error = self.query_one("#error-text", Static)

        target_dir = self.query_one("#target-dir", Input).value.strip()
        if not target_dir:
                error.update("Не все поля заполнены")
                return

        if self.action == "sort":
            sort_dir = self.query_one("#sort-dir", Input).value.strip()
            if not sort_dir:
                error.update("Не все поля заполнены")
                return
                
        error.update("")
        self.app.push_screen(ConfirmScreen(target_dir), self.on_confirm)

    def on_confirm(self, confirmed: bool):

        if not confirmed:
            return

        if self.action == "sort":
            sort_dir = self.query_one("#sort-dir", Input).value.strip()
            set_key(".env", "SORT_DIR", sort_dir)
            load_dotenv(dotenv_path=".env", override=True)

        target_dir = self.query_one("#target-dir", Input).value.strip()
        set_key(".env", "TARGET_DIR", target_dir)
        load_dotenv(dotenv_path=".env", override=True)


        if self.action == "create-links":
            target = create_links
        elif self.action == "sort":
            target = sort_files
  
        else:
            return
        
        self.app.push_screen("progress")
        Thread(target=target, daemon=True).start()
