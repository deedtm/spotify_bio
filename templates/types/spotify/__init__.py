from pydantic import BaseModel


class Spotify(BaseModel):
    track_line: str
    idle_line: str
    np: str
    nothing: str
    forward_post: str
    forward_post_again: str
    marker: str
    marker_set: str
    marker_missing: str
    post_missing: str
    post_link_bad: str
    updated: str


__all__ = "Spotify",
