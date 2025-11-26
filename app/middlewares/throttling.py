import time
from collections import defaultdict
from typing import Dict, Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Update


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit_updates: int, window_seconds: float):
        self.limit_updates = limit_updates
        self.window_seconds = window_seconds
        self.users_requests = defaultdict(list)

    async def __call__(
            self,
            handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:

        user_id = None
        if event.message:
            user_id = event.message.from_user.id
            event_obj = event.message
        elif event.callback_query:
            user_id = event.callback_query.from_user.id
            event_obj = event.callback_query
        else:
            return await handler(event, data)

        current_time = time.time()

        cutoff_time = current_time - self.window_seconds
        self.users_requests[user_id] = [
            ts for ts in self.users_requests[user_id]
            if ts > cutoff_time
        ]

        if len(self.users_requests[user_id]) >= self.limit_updates:
            i18n = data.get("i18n")
            if i18n:
                wait_time = int(cutoff_time + self.window_seconds - current_time)
                message = i18n.get("throttling-message", seconds=wait_time)

                if event.message:
                    await event.message.answer(message)
                elif event.callback_query:
                    await event.callback_query.answer(message, show_alert=True)
            return

        self.users_requests[user_id].append(current_time)
        return await handler(event, data)
