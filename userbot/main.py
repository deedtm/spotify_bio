import asyncio

from loguru import logger
from telethon import TelegramClient
from telethon.sessions import StringSession

from database.crud_managers import edit_crud

from .config import API_HASH, API_ID, SESSION_STRING

POLL_INTERVAL = 3


async def apply_edits(client: TelegramClient):
    while edit := await edit_crud.take():
        chat_id, message_id, html = edit.chat_id, edit.message_id, edit.html

        target_chat = int(chat_id) if chat_id.lstrip("-").isdigit() else chat_id

        try:
            await client.edit_message(target_chat, message_id, html, parse_mode="html")
            logger.info(f"Post {chat_id}/{message_id} edited")
        except Exception as e:
            logger.error(f"Edit {chat_id}/{message_id} failed: {e}")
        await edit_crud.update("id", edit.id, done=True)


async def main():
    if not SESSION_STRING:
        raise SystemExit("USERBOT_SESSION must be set in .env (run python -m userbot.get_session)")

    client = TelegramClient(
        StringSession(SESSION_STRING), API_ID, API_HASH, parse_mode="html"
    )
    await client.start()  # uses the session string, no interaction needed
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
