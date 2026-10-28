"""SMM-бот: калимаи рамзӣ дар шарҳҳои канал → ссилка ба директ.

Ҷараён:
1. Обуначӣ дар шарҳи пост калимаи рамзиро менависад.
2. Бот ба шарҳ бо тугмаи t.me/<bot>?start=<id> ҷавоб медиҳад
   (Telegram ба бот иҷозат намедиҳад, ки худаш аввал ба директ нависад).
3. Обуначӣ Start-ро пахш мекунад → бот обунаро месанҷад ва ссилкаро мефиристад.
"""

from __future__ import annotations

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F, Router
from aiogram.enums import ChatMemberStatus, ChatType
from aiogram.exceptions import TelegramBadRequest, TelegramForbiddenError
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    User,
)

from .config import Config, Keyword, load_config
from .matching import Cooldown, KeywordMatcher
from .storage import Storage

log = logging.getLogger("smm_bot")

COMMENT_REPLY = os.environ.get(
    "COMMENT_REPLY", "Ташаккур! Барои гирифтани мавод тугмаро пахш кунед 👇"
)
COMMENT_BUTTON = os.environ.get("COMMENT_BUTTON", "📩 Гирифтан")
NOT_SUBSCRIBED = os.environ.get(
    "NOT_SUBSCRIBED_TEXT",
    "Мавод танҳо барои обуначиёни канал аст. Обуна шавед ва «✅ Санҷидан»-ро пахш кунед.",
)
WELCOME = os.environ.get(
    "WELCOME_TEXT",
    "Салом! Дар шарҳҳои канал калимаи рамзиро нависед — ман маводро ба шумо мефиристам.",
)

SUBSCRIBED_STATUSES = {
    ChatMemberStatus.CREATOR,
    ChatMemberStatus.ADMINISTRATOR,
    ChatMemberStatus.MEMBER,
}


def channel_url(channel: str) -> str:
    return f"https://t.me/{channel.lstrip('@')}"


def build_router(
    config: Config, storage: Storage, matcher: KeywordMatcher, discussion: dict[str, int]
) -> Router:
    router = Router()
    cooldown = Cooldown(config.comment_cooldown)

    async def is_subscribed(bot: Bot, user_id: int) -> bool:
        if not config.require_subscription:
            return True
        try:
            member = await bot.get_chat_member(config.channel, user_id)
        except TelegramBadRequest:
            return False
        if member.status in SUBSCRIBED_STATUSES:
            return True
        # Корбари маҳдудшуда (restricted) метавонад узв бошад.
        return bool(getattr(member, "is_member", False))

    async def deliver(message: Message, user: User, keyword: Keyword) -> None:
        markup = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=keyword.button, url=keyword.url)]]
        )
        await message.answer(
            keyword.message.format(url=keyword.url),
            reply_markup=markup,
            disable_web_page_preview=False,
        )
        storage.save_delivery(user.id, keyword.id, user.username, user.first_name)
        log.info("Delivered %s to %s", keyword.id, user.id)

    def subscribe_markup(keyword: Keyword) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📢 Обуна шудан", url=channel_url(config.channel))],
                [InlineKeyboardButton(text="✅ Санҷидан", callback_data=f"check:{keyword.id}")],
            ]
        )

    @router.message(
        F.chat.type == ChatType.SUPERGROUP,
        F.func(lambda m: m.chat.id == discussion.get("id")),
    )
    async def on_comment(message: Message, bot: Bot) -> None:
        # Постҳои канал, ки худкор ба гурӯҳ меоянд, ва шарҳҳо «аз номи канал» сарфи назар мешаванд.
        if message.is_automatic_forward or message.sender_chat or not message.from_user:
            return
        if message.from_user.is_bot:
            return

        keyword = matcher.match(message.text or message.caption)
        if keyword is None:
            return
        if not cooldown.allow(message.from_user.id, keyword.id):
            return

        me = await bot.me()
        link = f"https://t.me/{me.username}?start={keyword.id}"
        await message.reply(
            COMMENT_REPLY,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text=COMMENT_BUTTON, url=link)]]
            ),
        )
        log.info("Keyword %s from %s in comments", keyword.id, message.from_user.id)

    @router.message(CommandStart(deep_link=True), F.chat.type == ChatType.PRIVATE)
    async def on_start_with_payload(message: Message, command: CommandObject, bot: Bot) -> None:
        keyword = config.keyword_by_id(command.args or "")
        if keyword is None or message.from_user is None:
            await message.answer(WELCOME)
            return
        if not await is_subscribed(bot, message.from_user.id):
            await message.answer(NOT_SUBSCRIBED, reply_markup=subscribe_markup(keyword))
            return
        await deliver(message, message.from_user, keyword)

    @router.message(CommandStart(), F.chat.type == ChatType.PRIVATE)
    async def on_start(message: Message) -> None:
        await message.answer(WELCOME)

    @router.callback_query(F.data.startswith("check:"))
    async def on_check(callback: CallbackQuery, bot: Bot) -> None:
        keyword = config.keyword_by_id(callback.data.split(":", 1)[1])
        if keyword is None or not isinstance(callback.message, Message):
            await callback.answer()
            return
        if not await is_subscribed(bot, callback.from_user.id):
            await callback.answer("Шумо ҳанӯз обуна нашудаед 🙂", show_alert=True)
            return
        await callback.answer("Ташаккур барои обуна!")
        try:
            await callback.message.delete()
        except TelegramBadRequest:
            pass
        await deliver(callback.message, callback.from_user, keyword)

    @router.message(Command("stats"), F.chat.type == ChatType.PRIVATE)
    async def on_stats(message: Message) -> None:
        if message.from_user is None or message.from_user.id not in config.admin_ids:
            return
        users, per_keyword = storage.stats()
        lines = [f"Корбарон: {users}"]
        lines += [f"• {keyword_id}: {count}" for keyword_id, count in per_keyword]
        await message.answer("\n".join(lines))

    return router


async def resolve_discussion_chat(bot: Bot, config: Config) -> int:
    if config.discussion_chat_id is not None:
        return config.discussion_chat_id
    chat = await bot.get_chat(config.channel)
    if chat.linked_chat_id is None:
        raise RuntimeError(
            f"Канали {config.channel} гурӯҳи шарҳҳо надорад. "
            "Дар танзимоти канал Discussion-ро фаъол кунед."
        )
    return chat.linked_chat_id


async def check_permissions(bot: Bot, config: Config, chat_id: int) -> None:
    me = await bot.me()
    try:
        member = await bot.get_chat_member(chat_id, me.id)
    except (TelegramBadRequest, TelegramForbiddenError):
        log.error(
            "Бот узви гурӯҳи шарҳҳо (%s) нест. Онро ба гурӯҳ илова карда, админ кунед.",
            chat_id,
        )
        return
    if member.status != ChatMemberStatus.ADMINISTRATOR:
        log.warning(
            "Бот дар гурӯҳи шарҳҳо админ нест — шарҳҳоро намебинад. Онро админ кунед."
        )


async def main() -> None:
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    config = load_config()
    storage = Storage(config.db_path)
    matcher = KeywordMatcher(config.keywords)

    bot = Bot(config.token)
    discussion = {"id": await resolve_discussion_chat(bot, config)}
    await check_permissions(bot, config, discussion["id"])

    me = await bot.me()
    log.info(
        "@%s оғоз шуд. Канал: %s, гурӯҳи шарҳҳо: %s, калимаҳо: %s",
        me.username,
        config.channel,
        discussion["id"],
        ", ".join(w for k in config.keywords for w in k.words),
    )

    dp = Dispatcher()
    dp.include_router(build_router(config, storage, matcher, discussion))
    # Агар webhook монда бошад, polling кор намекунад — онро тоза мекунем.
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
