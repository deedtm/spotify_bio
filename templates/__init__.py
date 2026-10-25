from .__utils import get_json_content
from .types import *

COMMANDS = Commands.model_validate_json(get_json_content("commands"))
EXCEPTIONS = Exceptions.model_validate_json(get_json_content("exceptions"))
MIDDLEWARES = Middlewares.model_validate_json(get_json_content("middlewares"))
SPOTIFY = Spotify.model_validate_json(get_json_content("spotify"))

__all__ = "COMMANDS", "EXCEPTIONS", "MIDDLEWARES", "SPOTIFY"
