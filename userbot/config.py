from dotenv import load_dotenv

load_dotenv()

import os

# fall back to pyrogram's built-in Telegram Desktop credentials: freshly created
# api_ids from my.telegram.org often get no login code delivered by Telegram
API_ID = int(os.getenv("USERBOT_API_ID", 611335))
API_HASH = os.getenv("USERBOT_API_HASH", "d524b414d21f4d37f08684c1df41ac13")
SESSION_STRING = os.getenv("USERBOT_SESSION")
