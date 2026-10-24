# Habit Tracker

A simple Python CLI habit tracker and Telegram bot.

## Install

Use Python 3.10 or newer:

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set `BOT_TOKEN` in a local `.env` file using `.env.example` as a guide, then run:

```sh
python bot.py
```

The CLI version can be run with `python main.py`. It uses the local data file; the Telegram bot stores each user's habits separately under `data/users/`.

Generated data, credentials, virtual environments, and Python bytecode are excluded from Git.
