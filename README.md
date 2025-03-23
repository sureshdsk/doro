# Doro - CLI based pomodoro app
Doro is a CLI based pomodoro app and countdown timer application built using python.

## Install
```bash
$ pip install doro
```

## Usage

### Pomodoro
#### Configuration
Configure pomodoro session using `doro config`. Config will be stored at `~/.doro.yaml`
```bash
$ doro config

# verify config
$ cat ~/.doro.yaml
```
#### Start Pomodoro
```bash
$ doro start
```

### Countdown timer
```bash
$ doro countdown MINUTES

# 15 minutes counter
$ doro countdown 15

# 90 minutes counter
$ doro countdown 90
```

## Demo
![pomodoro-demo](https://raw.githubusercontent.com/sureshdsk/doro/main/screenshots/doro-demo.gif?raw=true)
![countdown-demo](https://raw.githubusercontent.com/sureshdsk/doro/main/screenshots/doro-demo2.gif?raw=true)


## Development
```
$ uv venv --python=3.12
$ source .venv/bin/activate

$ uv build
Successfully built dist/doro-X.X.X.tar.gz
Successfully built dist/doro-X.X.X-py3-none-any.whl 

$ pip install dist/doro-0.0.4-py3-none-any.whl --force

$ doro --help
```