import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

import yaml

try:
    from yaml import CDumper as Dumper
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Dumper, Loader

CONFIG_PATH = os.path.join(Path.home(), ".doro.yaml") if os.name == 'nt'  else os.path.join(os.getenv("HOME"), ".doro.yaml")


@dataclass()
class RuntimeConfig:
    focus_minutes: str = "15"
    break_minutes: str = "5"
    terminal_color: str = "magenta"
    block_social_media: bool = False


def dump_config(config: Dict):
    with open(CONFIG_PATH, "w+") as f:
        f.write(yaml.dump(config, Dumper=Dumper, default_flow_style=False))


def load_config():
    if not Path(CONFIG_PATH).exists():
        return
    with open(CONFIG_PATH, "r") as f:
        config = yaml.load(f, Loader=Loader)
    return config


def get_config():
    config_yaml = load_config() or {"doro": {}}
    config = RuntimeConfig(**config_yaml["doro"])
    return config
