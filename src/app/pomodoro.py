import pathlib

import pyglet
from rich.console import Console
from rich.style import Style

from .config import RuntimeConfig
from .progress import show_progress_bar
from .proxy import start_proxy_in_background, stop_proxy

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
        self.proxy_active = False

        self.console.clear()
        self.console.print(APP_TITLE)

    @property
    def music(self):
        _music = pyglet.media.load(
            f"{pathlib.Path(__file__).parent.resolve()}/sounds/{self.sound_title}.wav",
            streaming=True,
        )
        return _music

    def play_music(self):
        self.music.play()
        pyglet.app.event_loop.sleep(1)

    def start_social_media_blocker(self):
        """Start the social media blocking proxy if enabled in config"""
        if not self.config.block_social_media:
            self.console.print("Social media blocking is disabled in configuration.")
            return
            
        self.console.print("Starting social media blocker...")
        proxy_started = start_proxy_in_background()
        if proxy_started:
            self.proxy_active = True
            self.console.print("Social media blocker activated! Focus mode enabled.")
        else:
            self.console.print("Failed to start social media blocker. Continuing without blocking.")

    def stop_social_media_blocker(self):
        """Stop the social media blocking proxy"""
        if self.proxy_active:
            stop_proxy()
            self.proxy_active = False
            self.console.print("Social media blocker deactivated.")

    def run_countdown(self):
        self.start_social_media_blocker()
        self.console.print("Running countdown...")
        show_progress_bar(self.config.focus_minutes)
        self.play_music()
        self.console.print(
            "\nCountdown timer has ended ⏰\n",
        )
        self.stop_social_media_blocker()

    def run_pomodoro(self):
        self.start_social_media_blocker()
        self.console.print("Running pomodoro...")
        show_progress_bar(self.config.focus_minutes)
        self.play_music()

        # Stop the blocker before asking for input
        self.stop_social_media_blocker()

        take_a_break = self.console.input(
            "\nAwesome! Take a break now? [ y/n ]: ",
        )

        if take_a_break.strip().lower() in ("y", "yes"):
            show_progress_bar(self.config.break_minutes)
            self.play_music()

        self.console.print(
            "\nCongrats!!! You've completed a pomodoro session! 🚀\n",
        )
