import os
import re

from aiogram.client.default import DefaultBotProperties

from config import cfg

######### [config.ini]
PARSE_MODE = cfg.get("telegram", "parse_mode")
DISABLE_LINK_PREVIEW = cfg.getboolean("telegram", "disable_link_preview")
DROP_PENDING_UPDATES = cfg.getboolean("telegram", "drop_pending_updates")

DEFAULT_BOT_PROPERTIES = DefaultBotProperties(
    parse_mode=PARSE_MODE, link_preview_is_disabled=DISABLE_LINK_PREVIEW
)

BACK_PREFIX = cfg.get("telegram", "back_prefix")
USERS_LIST_AMOUNT = cfg.getint("telegram", "users_list_amount")

TRACK_MARKER = cfg.get("spotify", "track_marker")
UPDATE_INTERVAL = cfg.getint("spotify", "update_interval")

ACCESSES = {k: int(v) for k, v in cfg.items("accesses")}

TOKEN = os.getenv("BOT_TOKEN")
_RAW_ACCESSES = os.getenv("ACCESSES")
USERS_ACCESSES = {
    int(k): ACCESSES.get(v.lower(), 0)
    for k, v in (u.split(":") for u in _RAW_ACCESSES.split())
}

######### [spotify]

_POST_LINK_RE = re.compile(r"^(?:https?://)?t\.me/(?:(c/)(\w+)|(\w+))/(\d+)$")


def parse_post_link(link: str) -> tuple[str, int] | None:
    """Parse a t.me post link into (chat_id, message_id)"""
    if not (match := _POST_LINK_RE.match(link.strip())):
        return None
    private, internal_chat, username, message_id = match.groups()
    # t.me/c/<internal_id> links use the internal id, the full chat id is -100<internal_id>
    chat = "-100" + internal_chat if private else username
    return chat, int(message_id)


POST_LINK = parse_post_link(os.getenv("POST_LINK", ""))
