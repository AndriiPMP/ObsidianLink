from textual.app import App
from tui.screens.option_screen import OptionScreen
from tui.screens.adress_screen import AdressScreen
from tui.screens.progress_screen import ProgressScreen
from tui.screens.loading_screen import LoadingScreen

CSS_PATH = "app_style.tcss"

class ObsidianAuto(App):
    SCREENS = {
        "option": OptionScreen,
        "adress": AdressScreen,
        "progress": ProgressScreen,
    }

    def on_mount(self) -> None:
        self.push_screen("option")

    def _go_home(self):
        while self.app.screen.name != "option":
            self.app.pop_screen()


if __name__ == "__main__":
    ObsidianAuto().run()
