import time

from ..connect import get_session
from ..models import Edit
from .base import CRUDBase


class EditCRUD(CRUDBase[Edit]):
    model = Edit

    async def push(self, chat_id: str, message_id: int, html: str) -> Edit:
        return await self.add(
            chat_id=chat_id,
            message_id=message_id,
            html=html,
            created_at=int(time.time()),
        )

    async def take_latest(self) -> list[Edit]:
        """Return the newest not-done edit for every post, dropping older queued ones"""
        async for session in get_session():
            from sqlalchemy import select

            stmt = (
                select(self.model)
                .where(self.model.done == False)  # noqa: E712
                .order_by(self.model.id)
            )
            edits = (await session.scalars(stmt)).all()

            latest: dict[tuple, Edit] = {}
            for edit in edits:
                latest[(edit.chat_id, edit.message_id)] = edit
            return list(latest.values())
        return []


edit_crud = EditCRUD(get_session)

__all__ = "edit_crud", "Edit",
