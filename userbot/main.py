import asyncio
import re

from loguru import logger
from pyrogram import Client, enums

from database.crud_managers import edit_crud, post_crud

from .config import API_HASH, API_ID, SESSION_STRING

POLL_INTERVAL = 3

_TG_EMOJI_RE = re.compile(r'<tg-emoji emoji-id="(\d+)">(.*?)</tg-emoji>')


def to_pyrogram_html(text: str) -> str:
    """aiogram renders premium emoji as <tg-emoji>, pyrogram expects <emoji>"""
    return _TG_EMOJI_RE.sub(r'<emoji id="\1">\2</emoji>', text)


async def apply_edits(client: Client):
    while edit := await edit_crud.take():
        chat_id, message_id, html = edit.chat_id, edit.message_id, edit.html

        if chat_id.lstrip("-").isdigit():
            target_chat = int(chat_id)
        else:
            target_chat = chat_id

        try:
            await client.edit_message_text(
                chat_id=target_chat,
                message_id=message_id,
                text=to_pyrogram_html(html),
                parse_mode=enums.ParseMode.HTML,
            )
            logger.info(f"Post {chat_id}/{message_id} edited")
            await edit_crud.update(edit.id, done=True)
        except Exception as e:
            logger.error(f"Edit {chat_id}/{message_id} failed: {e}")
            await edit_crud.update(edit.id, done=True)


async def main():
    if not (API_ID and API_HASH and SESSION_STRING):
        raise SystemExit("USERBOT_API_ID, USERBOT_API_HASH and USERBOT_SESSION must be set in .env")

    client = Client(
        "spotify_bio_userbot",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING,
        parse_mode=enums.ParseMode.HTML,
    )
    await client.start()
    me = await client.get_me()
    logger.info(f"USERBOT STARTED {me.id}:{me.username}")

    while True:
        try:
            await apply_edits(client)
        except Exception as e:
            logger.error(f"Userbot loop error: {e}")
        await asyncio.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
