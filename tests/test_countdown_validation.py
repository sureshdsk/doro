"""Non-positive countdown durations must be rejected instead of silently finishing instantly."""

from typer.testing import CliRunner

from app import pomodoro as pomodoro_module
from app.cli import app
from app.config import RuntimeConfig

runner = CliRunner()


def _patched_config(monkeypatch):
    monkeypatch.setattr(
        "app.cli.get_config",
        lambda: RuntimeConfig(
            focus_minutes="15",
            break_minutes="5",
            terminal_color="magenta",
            block_social_media=False,
        ),
    )
    # Keep the test hermetic: never run the real timer or sound.
    monkeypatch.setattr(pomodoro_module, "show_progress_bar", lambda minutes: None)
    monkeypatch.setattr(pomodoro_module.Pomodoro, "play_music", lambda self: None)


def test_countdown_rejects_zero_minutes(monkeypatch):
    _patched_config(monkeypatch)
    result = runner.invoke(app, ["countdown", "0"])
    assert result.exit_code == 1
    assert "at least 1" in result.output


def test_countdown_rejects_negative_minutes(monkeypatch):
    _patched_config(monkeypatch)
    result = runner.invoke(app, ["countdown", "--", "-5"])
    assert result.exit_code == 1
    assert "at least 1" in result.output
