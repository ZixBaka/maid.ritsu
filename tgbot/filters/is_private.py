import typing

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message


class IsPrivate(BoundFilter):
    key = "is_private"

    def __init__(self, is_private=typing.Optional[bool]):
        self.is_private = is_private

    async def check(self, obj, *args):
        if self.is_private is True:
            return types.ChatType.PRIVATE == obj.chat.type
        else:
            return True


class CallIsPrivate(BoundFilter):
    key = "call_is_private"

    def __init__(self, call_is_private=typing.Optional[bool]):
        self.call_is_private = call_is_private

    async def check(self, obj, *args):
        if self.call_is_private is True:
            return types.ChatType.PRIVATE == obj.message.chat.type
        else:
            return True

