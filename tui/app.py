from textual.app import App
from tui.screens.option_screen import OptionScreen

CSS_PATH = "app_style.tcss"

class ObsidianAuto(App):
    def compose(self):
        if False:
            yield

    def on_mount(self) -> None:
        self.push_screen(OptionScreen())


if __name__ == "__main__":
    ObsidianAuto().run()
