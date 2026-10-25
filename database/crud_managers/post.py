from ..models import Post
from ..connect import get_session
from .base import CRUDBase


class PostCRUD(CRUDBase[Post]):
    model = Post


post_crud = PostCRUD(get_session)

__all__ = "post_crud", "Post"
