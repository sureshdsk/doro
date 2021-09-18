import pathlib

import pyglet
from rich.console import Console
from rich.style import Style

from .config import RuntimeConfig
from .progress import show_progress_bar

APP_TITLE = """
┏━━━┓
┗┓┏┓┃
╋┃┃┃┣━━┳━┳━━┓
╋┃┃┃┃┏┓┃┏┫┏┓┃
┏┛┗┛┃┗┛┃┃┃┗┛┃
┗━━━┻━━┻┛┗━━┛
"""


class Pomodoro:
    def __init__(self, config: RuntimeConfig, sound_title="ding"):
        self.sound_title = sound_title
        self.config = config
        self.console = Console(style=Style(color=self.config.terminal_color))

        self.console.clear()
        self.console.print(APP_TITLE)

    @property
    def music(self):
        _music = pyglet.media.load(
            f"{pathlib.Path(__file__).parent.resolve()}"
            f"/sounds/{self.sound_title}.wav",
            streaming=True,
        )
        return _music

    def play_music(self):
        self.music.play()
        pyglet.app.event_loop.sleep(1)

    def run_countdown(self):
        self.console.print("Running countdown...")
        show_progress_bar(self.config.focus_minutes)
        self.play_music()
        self.console.print(
            "\nCountdown timer has ended ⏰\n",
        )

    def run_pomodoro(self):
        self.console.print("Running pomodoro...")
        show_progress_bar(self.config.focus_minutes)
        self.play_music()

        take_a_break = self.console.input(
            "\nAwesome! Take a break now? [ y/n ]: ",
        )

        if take_a_break.strip().lower() in ("y", "yes"):
            show_progress_bar(self.config.break_minutes)
            self.play_music()

        self.console.print(
            "\nCongrats!!! You've completed a pomodoro session! 🚀\n",
        )
