# Spotify Bio Bot

Telegram bot that takes the currently playing track from Spotify and updates one line in a channel post, leaving everything else in the post untouched.

Based on [aiogram_base_bot](https://github.com/deedtm/aiogram_base_bot).

## Features

- aiogram3 + PostgreSQL + Docker (same base as aiogram_base_bot)
- Updates the "now playing" line in a channel post every N seconds
- Edits **only** the marker line, found by text, not by line number
- Premium emojis and links in the post stay intact (the post is edited as HTML)
- Pause/absence of playback shows a short idle line instead of the track

## Setup

1. `cp config.ini.example config.ini` and `cp .env.example .env`, fill both in
2. Create an app at https://developer.spotify.com/dashboard with redirect URI `http://127.0.0.1:8899/callback`
3. Run `python spotify/get_token.py`, log in and copy the printed refresh token into `.env`
4. Add the bot to your channel as an admin with "edit messages" permission
5. Put a track line with the marker (default `🎧`) into your post
6. Forward the post to the bot with the `/setpost` command — the bot saves its exact HTML
7. `docker-compose up --build -d`

## Commands (owner only)

| Command | Description |
| --- | --- |
| `/setpost` | Forward the channel post here to register it for editing |
| `/np` | Show the current Spotify track |
| `/npcheck` | Force a post update right now |
| `/setmarker` | Change the marker string (updates config.ini) |

## Configuration

- `config.ini` `[spotify]`: `track_marker` (the string the bot looks for in the post), `update_interval` (seconds between checks)
- `.env`: `BOT_TOKEN`, `SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`, `SPOTIFY_REFRESH_TOKEN`, `POST_LINK` (optional safety check that the forwarded post is the right one)
- `templates/jsons/spotify.json`: all message templates, including how the track line looks (`track_line` uses `{artist}`, `{name}`, `{url}`) and the idle line (`idle_line`)

## Notes

- The bot never touches lines without the marker; if the marker line is missing, it just skips the update
- If you edit the post manually (e.g. add links), forward it to the bot again with `/setpost` so it picks up the fresh HTML
