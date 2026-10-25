from dataclasses import dataclass

import aiohttp

from .config import CURRENTLY_PLAYING_URL
from .token import get_token


@dataclass(frozen=True)
class Track:
    artist: str
    name: str
    url: str
    is_playing: bool


async def get_current_track() -> Track | None:
    """Return the currently playing track, or None if nothing is playing"""
    token = await get_token()

    async with aiohttp.ClientSession() as session:
        async with session.get(
            CURRENTLY_PLAYING_URL, headers={"Authorization": f"Bearer {token}"}
        ) as resp:
            if resp.status == 204:
                return None
            body = await resp.json()
            if resp.status != 200:
                raise RuntimeError(f"currently-playing failed ({resp.status}): {body}")

    item = body["item"]
    return Track(
        artist=", ".join(a["name"] for a in item["artists"]),
        name=item["name"],
        url=item["external_urls"]["spotify"],
        is_playing=bool(body["is_playing"]),
    )
