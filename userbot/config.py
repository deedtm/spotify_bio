from dotenv import load_dotenv

load_dotenv()

import os

API_ID = int(os.getenv("USERBOT_API_ID", 2040))
API_HASH = os.getenv("USERBOT_API_HASH", "b18441a1ff607e10a989891a5462e627")
SESSION_STRING = os.getenv("USERBOT_SESSION")
