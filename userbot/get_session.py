"""
One-time login script for the userbot via QR code (no login code needed).

python -m userbot.get_session

Scan the QR from Telegram: Settings -> Devices -> Link Desktop Device.
Copy the printed session string into .env (USERBOT_SESSION)
"""
import asyncio

import qrcode
from telethon import TelegramClient
from telethon.sessions import StringSession

from .config import API_HASH, API_ID


def print_qr(url: str):
    code = qrcode.QRCode(border=1)
    code.add_data(url)
    code.make()
    code.print_ascii()


async def main():
    client = TelegramClient(StringSession(), API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        qr = await client.qr_login()
        print("Scan this QR from Telegram: Settings -> Devices -> Link Desktop Device\n")
        print_qr(qr.url)
        print("(the QR refreshes automatically every ~30 seconds)")

        while not qr.token_alive:
            try:
                await qr.wait()
            except asyncio.TimeoutError:
                await qr.recreate()
                print_qr(qr.url)

        me = await client.get_me()
        print(f"\nLogged in as {me.first_name} (@{me.username})")

    print("\nAdd this line to your .env:\n")
    print(f"USERBOT_SESSION={client.session.save()}")


if __name__ == "__main__":
    asyncio.run(main())
