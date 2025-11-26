from aiogram import BaseMiddleware
from typing import Any, Dict, Callable, Awaitable
from aiogram.types import Update, Message, CallbackQuery
from app.config import get_middleware_logger


class LoggingMiddleware(BaseMiddleware):
    def __init__(self, logger=None):
        self.logger = logger or get_middleware_logger("logging")
        super().__init__()

    async def __call__(
        self, handler: Callable, event: Update, data: Dict[str, Any]
    ) -> Any:
        event_info = self._get_event_info(event)

        self.logger.info(f"<<< incoming: {event_info}")

        try:
            result = await handler(event, data)
            self.logger.info(f">>> processed: {event_info}")
            return result

        except Exception as e:
            self.logger.error(f"❌ ERROR processing {event_info}: {str(e)}")
            raise

    def _get_event_info(self, event: Update) -> str:
        event_type = type(event).__name__
        user_info = self._get_user_info(event)
        chat_info = self._get_chat_info(event)
        content_info = self._get_content_info(event)

        return f"{user_info} | {chat_info} | {content_info}"

    def _get_user_info(self, event: Update) -> str:
        """Извлекает информацию о пользователе"""
        user = None

        if event.message:
            user = event.message.from_user
        elif event.callback_query:
            user = event.callback_query.from_user
        elif event.chat_member:
            user = event.chat_member.from_user
        elif event.my_chat_member:
            user = event.my_chat_member.from_user
        elif event.edited_message:
            user = event.edited_message.from_user
        elif event.channel_post:
            user = event.channel_post.from_user
        elif event.edited_channel_post:
            user = event.edited_channel_post.from_user
        elif event.inline_query:
            user = event.inline_query.from_user
        elif event.chosen_inline_result:
            user = event.chosen_inline_result.from_user
        elif event.shipping_query:
            user = event.shipping_query.from_user
        elif event.pre_checkout_query:
            user = event.pre_checkout_query.from_user
        elif event.poll_answer:
            user = event.poll_answer.user
        elif event.chat_join_request:
            user = event.chat_join_request.from_user

        if user:
            username = f"@{user.username}" if user.username else "no_username"
            first_name = f"{user.first_name}"
            last_name = user.last_name if user.last_name else None
            name = first_name + (" " + last_name if last_name else "")
            return f"👤 {name} ({username}, {user.id})"
        else:
            return "👤 ?"

    def _get_chat_info(self, event: Update) -> str:
        """Извлекает информацию о чате"""
        chat = None

        if event.message:
            chat = event.message.chat
        elif event.callback_query and event.callback_query.message:
            chat = event.callback_query.message.chat
        elif event.chat_member:
            chat = event.chat_member.chat
        elif event.my_chat_member:
            chat = event.my_chat_member.chat
        elif event.edited_message:
            chat = event.edited_message.chat
        elif event.channel_post:
            chat = event.channel_post.chat
        elif event.edited_channel_post:
            chat = event.edited_channel_post.chat
        elif event.chat_join_request:
            chat = event.chat_join_request.chat

        if chat:
            chat_id = chat.id
            chat_type = chat.type if hasattr(chat, "type") else "unknown"
            chat_title = getattr(
                chat, "title", getattr(chat, "username", f"ID:{chat.id}")
            )
            if chat_type == "private":
                chat_info = f"💬"
            else:
                chat_info = f"💬 {chat_type} {chat_id}"
            if not chat_title is None:
                chat_info += f" ({chat_title})"
            return chat_info
        else:
            return "💬 no_chat"

    def _get_content_info(self, event: Update) -> str:
        """Извлекает информацию о содержимом события"""
        if event.message:
            if event.message.text:
                text_preview = (
                    event.message.text[:50] + "..."
                    if len(event.message.text) > 50
                    else event.message.text
                )
                return f"(📝) {text_preview}"
            elif event.message.photo:
                return "🖼️ Photo"
            elif event.message.document:
                return "📎 Document"
            elif event.message.sticker:
                return "😀 Sticker"
            else:
                return f"📦 {event.message.content_type}"
        elif event.callback_query:
            return f"🔘 Callback: {event.callback_query.data}"
        elif event.chat_member:
            return "👥 Chat member update"
        elif event.my_chat_member:
            return f"🤖 Bot chat member update"
        else:
            return "📨 Other event"
