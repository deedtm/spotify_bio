import asyncio
from html import escape

from aiogram import Bot
from loguru import logger

from database.crud_managers import edit_crud, post_crud
from spotify.api import Track, get_current_track
from templates import SPOTIFY as tmpl

from .config import TRACK_MARKER, UPDATE_INTERVAL


def render_track_line(track: Track | None) -> str:
    if track is None or not track.is_playing:
        return tmpl.idle_line
    return tmpl.track_line.format(
        url=track.url, artist=escape(track.artist), name=escape(track.name)
    )


def replace_marker_line(text: str, marker: str, new_line: str) -> str | None:
    """Replace every line containing the marker, leaving everything else untouched.
    Returns the new text, or None if the marker line was not found"""
    lines = text.split("\n")
    found = False
    for i, line in enumerate(lines):
        if marker in line:
            lines[i] = new_line
            found = True
    return "\n".join(lines) if found else None


async def update_post(bot: Bot) -> bool:
    """Queue an update of the marker line; the userbot applies it (Bot API
    strips premium emoji in channel messages, so the edit goes through MTProto)"""
    post = await post_crud.get_one()
    if post is None:
        logger.warning("No post stored yet, forward the post to the bot via /setpost")
        return False

    track = await get_current_track()
    if track is not None:
        logger.debug(f"Spotify: {track.artist} — {track.name} (playing={track.is_playing})")
    else:
        logger.debug("Nothing is playing on Spotify")

    track_line = render_track_line(track)
    new_text = replace_marker_line(post.html, TRACK_MARKER, track_line)
    if new_text is None:
        logger.warning(f"Marker {TRACK_MARKER!r} not found in the post, skipping")
        return False
    if new_text == post.html:
        logger.debug("Track line is up to date, skipping")
        return False

    await edit_crud.push(post.chat_id, post.message_id, new_text)
    await post_crud.update(post.id, html=new_text)
    logger.info(f"Edit queued: {track_line}")
    return True


async def updater_loop(bot: Bot):
    logger.info(f"Updater started (interval={UPDATE_INTERVAL}s, marker={TRACK_MARKER!r})")
    while True:
        try:
            await update_post(bot)
        except Exception as e:
            logger.error(f"Updater error: {e}")
        await asyncio.sleep(UPDATE_INTERVAL)
