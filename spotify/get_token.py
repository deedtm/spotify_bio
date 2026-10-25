"""
One-time authorization script for the Spotify Web API.

1. Create an app at https://developer.spotify.com/dashboard
2. Set the redirect URI to http://127.0.0.1:8899/callback
3. Put SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET into .env
4. Run: python spotify/get_token.py
5. Copy the printed refresh token into .env (SPOTIFY_REFRESH_TOKEN)
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlencode
from urllib.request import Request, urlopen

from base64 import b64encode

from dotenv import load_dotenv

load_dotenv()

from os import getenv

CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://127.0.0.1:8899/callback"
SCOPES = "user-read-currently-playing user-read-playback-state"
PORT = 8899


def main():
    params = urlencode(
        {
            "client_id": CLIENT_ID,
            "response_type": "code",
            "redirect_uri": REDIRECT_URI,
            "scope": SCOPES,
        }
    )
    print("Open this URL in your browser and log in:\n")
    print(f"https://accounts.spotify.com/authorize?{params}\n")

    code = None

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            nonlocal code
            code = parse_qs(self.path.split("?")[1]).get("code", [None])[0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"You can close this tab now")

    server = HTTPServer(("127.0.0.1", PORT), Handler)
    print(f"Waiting for callback on port {PORT}...")
    server.handle_request()

    if not code:
        raise SystemExit("No authorization code received")

    auth = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    body = urlencode(
        {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        }
    ).encode()
    req = Request(
        "https://accounts.spotify.com/api/token",
        data=body,
        headers={"Authorization": f"Basic {auth}"},
    )
    resp = urlopen(req)
    import json

    print("\nAdd this line to your .env:\n")
    print(f"SPOTIFY_REFRESH_TOKEN={json.loads(resp.read())['refresh_token']}")


if __name__ == "__main__":
    main()
