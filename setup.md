

uv venv --python=3.12
uv pip install --force-reinstall -r requirements.txt
uv pip install --upgrade mitmproxy flask werkzeug
which mitmdump


mitmdump -s /Users/dsk/.doro_scripts/social_media_blocker.py --listen-port 8080