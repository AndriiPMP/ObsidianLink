from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Button

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