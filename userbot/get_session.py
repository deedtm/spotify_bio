"""
One-time login script for the userbot. Run it locally, enter the phone number
and the code from Telegram, then copy the printed session string into .env

python -m userbot.get_session
"""
import asyncio

from pyrogram import Client

from .config import API_HASH, API_ID

SESSION_NAME = "spotify_bio_userbot"


async def main():
    async with Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH) as client:
        me = await client.get_me()
        session_string = await client.export_session_string()
        print(f"\nLogged in as {me.first_name} (@{me.username})")
        print("\nAdd this line to your .env:\n")
        print(f"USERBOT_SESSION={session_string}")


if __name__ == "__main__":
    asyncio.run(main())
