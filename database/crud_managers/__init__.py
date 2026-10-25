from ..connect import get_session
from .edit import Edit, EditCRUD, edit_crud
from .post import Post, PostCRUD, post_crud
from .user import User, UserCRUD

user_crud = UserCRUD(get_session)

__all__ = (
    "user_crud",
    "User",
    "post_crud",
    "PostCRUD",
    "Post",
    "edit_crud",
    "EditCRUD",
    "Edit",
)
