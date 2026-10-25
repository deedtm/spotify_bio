from os import getenv

CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = getenv("SPOTIFY_REFRESH_TOKEN")

TOKEN_URL = "https://accounts.spotify.com/api/token"
CURRENTLY_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"
