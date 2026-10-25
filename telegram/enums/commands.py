from dataclasses import dataclass


@dataclass(frozen=True)
class Commands:
    class np:
        desc = "show the current Spotify track"
        access = 1

    class npcheck:
        desc = "update the channel post right now"
        access = 1

    class setmarker:
        desc = "change the track line marker in the post"
        access = 3


def parse_commands(command_format: str, access_level: int) -> list[str]:
    parsed_commands = [
        command_format.format(
            command='/' + name,
            args=getattr(c, "args", "") + " ",
            description=c.desc,
        )
        for name, c in Commands.__dict__.items()
        if not name.startswith("__") and c.access <= access_level
    ]
    return parsed_commands
