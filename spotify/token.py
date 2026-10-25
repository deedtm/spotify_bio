import time

import aiohttp
from loguru import logger

from .config import CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN, TOKEN_URL

_access_token: str | None = None
_expires_at: float = 0


async def get_token() -> str:
    """Return a valid access token, refreshing it if needed"""
    global _access_token, _expires_at

    if _access_token and time.time() < _expires_at - 60:
        return _access_token

    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            TOKEN_URL, data=data, auth=aiohttp.BasicAuth(CLIENT_ID, CLIENT_SECRET)
        ) as resp:
            body = await resp.json()
            if resp.status != 200:
                raise RuntimeError(f"token refresh failed ({resp.status}): {body}")

    _access_token = body["access_token"]
    _expires_at = time.time() + body["expires_in"]
    logger.debug("Spotify access token refreshed")
    return _access_token
