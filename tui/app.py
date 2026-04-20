from textual.app import App
from tui.screens import StageScreen

CSS_PATH = "app_style.tcss"

class ObsidianAuto(App):
    
    def compose(self):
        if False:
            yield

          
    def on_mount(self) -> None:
        self.push_screen(StageScreen(), self.on_stage_selected)


    def on_stage_selected(self, stage):
        print(stage)




if __name__ == "__main__":
    ObsidianAuto().run()
