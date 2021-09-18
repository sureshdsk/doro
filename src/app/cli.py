import typer
from rich.prompt import Prompt

from .config import dump_config
from .config import get_config
from .constants import BREAK_MINUTES
from .constants import FOCUS_MINUTES
from .constants import TERMINAL_COLORS
from .pomodoro import Pomodoro

app = typer.Typer()


@app.command()
def config():
    duration = Prompt.ask(
        "Enter your focus duration: ",
        choices=FOCUS_MINUTES,
        default="15",
    )
    break_minutes = Prompt.ask(
        "Enter your break duration: ",
        choices=BREAK_MINUTES,
        default="5",
    )
    terminal_color = Prompt.ask(
        "Enter your font color: ",
        choices=TERMINAL_COLORS,
        default="magenta",
    )

    config = {
        "doro": {
            "focus_minutes": duration,
            "break_minutes": break_minutes,
            "terminal_color": terminal_color,
        },
    }
    dump_config(config)


@app.command()
def start():
    config = get_config()
    session = Pomodoro(config)
    session.run_pomodoro()


@app.command()
def countdown(minutes: int = typer.Argument(15)):
    config = get_config()
    config.focus_minutes = minutes
    session = Pomodoro(config)
    session.run_countdown()


if __name__ == "__main__":
    app()
