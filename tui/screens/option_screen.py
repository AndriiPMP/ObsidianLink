from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label, ListItem, ListView
from tui.screens.adress_screen import AdressScreen

class OptionScreen(Screen): 

    def compose(self) -> ComposeResult:
        yield ListView(
            ListItem(Label("Создание связей"), id="create-links"),
            ListItem(Label("Сортировка"), id="sort"),
            id="options-list",
        )

    def on_mount(self) -> None:
        self.query_one("#options-list", ListView).index = 0
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.item.id == "create-links":
            self.app.push_screen(AdressScreen())
