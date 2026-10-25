from pydantic import BaseModel


class Commands(BaseModel):
    start: str
    access: str


__all__ = "Commands",
