import time

from rich.progress import track

from .constants import WAIT_FOR_SECONDS


def show_progress_bar(minutes):
    seconds = int(minutes) * 60
    progress_conf = {
        "refresh_per_second": 1,
        "auto_refresh": False,
        "description": None,
    }
    for _ in track(range(seconds), **progress_conf):
        time.sleep(WAIT_FOR_SECONDS)
