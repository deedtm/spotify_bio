from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

import telegram.config as tg_config
from config import cfg
from database.crud_managers import post_crud
from spotify.api import get_current_track
from templates import EXCEPTIONS as tmpl_ex
from templates import SPOTIFY as tmpl

from ...config import ACCESSES, POST_LINK
from ...filters.access_level import AccessLevelFilter
from ...objects import router
from ...states.track import TrackState
from ...updater import replace_marker_line, update_post


@router.message(AccessLevelFilter(ACCESSES["owner"]), Command("setpost"))
async def setpost_handler(msg: Message, state: FSMContext):
    await msg.answer(tmpl.forward_post)
    await state.set_state(TrackState.post)


@router.message(AccessLevelFilter(ACCESSES["owner"]), TrackState.post)
async def setpost_state(msg: Message, state: FSMContext):
    """Owner forwards the channel post here to let the bot edit it"""
    await state.clear()
    fwd = msg.forward_from_chat
    if fwd is None or msg.forward_from_message_id is None:
        await msg.answer(tmpl.forward_post_again)
        return

    if POST_LINK is not None:
        expected_chat, expected_message = POST_LINK
        if str(fwd.id) != str(expected_chat) or msg.forward_from_message_id != expected_message:
            await msg.answer(tmpl.post_link_bad.format(POST_LINK))
            return

    html = msg.html_text
    if tg_config.TRACK_MARKER not in html:
        await msg.answer(tmpl.marker_missing)
        return

    if post := await post_crud.get_one():
        await post_crud.delete("id", post.id)
    await post_crud.add(chat_id=fwd.id, message_id=msg.forward_from_message_id, html=html)

    await msg.answer(tmpl.marker_set.format(tg_config.TRACK_MARKER))


@router.message(AccessLevelFilter(ACCESSES["owner"]), Command("np"))
async def np_handler(msg: Message):
    track = await get_current_track()
    if track is None or not track.is_playing:
        await msg.answer(tmpl.nothing)
        return
    await msg.answer(tmpl.np.format(track.artist, track.name, track.url))


@router.message(AccessLevelFilter(ACCESSES["owner"]), Command("npcheck"))
async def npcheck_handler(msg: Message):
    if not await update_post(msg.bot):
        return
    post = await post_crud.get_one()
    line = next((l for l in post.html.split("\n") if tg_config.TRACK_MARKER in l), "")
    await msg.answer(tmpl.updated.format(line))


@router.message(AccessLevelFilter(ACCESSES["owner"]), Command("setmarker"))
async def setmarker_handler(msg: Message, state: FSMContext):
    await msg.answer(tmpl.marker.format(tg_config.TRACK_MARKER))
    await state.set_state(TrackState.marker)


@router.message(AccessLevelFilter(ACCESSES["owner"]), TrackState.marker)
async def setmarker_state(msg: Message, state: FSMContext):
    await state.clear()
    old_marker = tg_config.TRACK_MARKER
    new_marker = msg.text.strip()

    cfg.set("spotify", "track_marker", new_marker)
    with open("config.ini", "w", encoding="utf-8") as f:
        cfg.write(f)
    tg_config.TRACK_MARKER = new_marker

    if post := await post_crud.get_one():
        if old_marker in post.html:
            line = next(
                (l for l in post.html.split("\n") if old_marker in l), None
            )
            if line is not None:
                new_line = line.replace(old_marker, new_marker)
                new_html = replace_marker_line(post.html, old_marker, new_line)
                await msg.bot.edit_message_text(
                    new_html, chat_id=post.chat_id, message_id=post.message_id
                )
                await post_crud.update(post.id, html=new_html)

    await msg.answer(tmpl.marker_set.format(new_marker))
