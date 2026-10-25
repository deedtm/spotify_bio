from pydantic import BaseModel


class Exceptions(BaseModel):
    base: str
    retry: str
    no_args: str
    wrong_args: str
    user_not_found: str
    own_access: str
    low_access_to_set: str
    over_access_set: str


__all__ = "Exceptions",
