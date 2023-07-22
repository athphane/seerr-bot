import ast
from configparser import ConfigParser
from functools import wraps

from pyrogram import Client
from pyrogram.raw.all import layer
from pyrogram.types import Message, CallbackQuery


class OverseerrBot(Client):
    def __init__(self):
        self.version = 1
        self.name = self.__class__.__name__.lower()

        self.config = ConfigParser()
        self.config.read('config.ini')

        super().__init__(
            'overseerrbot',
            api_id=self.config.get('pyrogram', 'api_id'),
            api_hash=self.config.get('pyrogram', 'api_hash'),
            bot_token=self.config.get('pyrogram', 'bot_token'),
            device_model='CoMpUtEr',
            workers=4,
            plugins=dict(root='overseerrbot/plugins'),
            workdir="./"
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        print(f"{self.__class__.__name__} v{self.version} (Layer {layer}) started on @{me.username}.\n"
              f"Let's accept all these fucking requests!")

    async def stop(self, *args):
        await super().stop()
        print(f"{self.__class__.__name__} stopped. Bye.")

    def admins(self):
        return ast.literal_eval(self.config.get(self.name, 'admins'))

    def is_admin(self, entity: Message or CallbackQuery) -> bool:
        user_id = entity.from_user.id

        return user_id in self.admins()

    @staticmethod
    def admins_only(func):
        @wraps(func)
        async def decorator(bot: OverseerrBot, message: Message):
            if bot.is_admin(message):
                await func(bot, message)

        decorator.admin = True

        return decorator

    @staticmethod
    def user_mentionable(entity: Message or CallbackQuery):
        if entity.from_user.username:
            user_mentionable = f"@{entity.from_user.username}"
        else:
            if entity.from_user.last_name:
                name_string = f"{entity.from_user.first_name} {entity.from_user.last_name}"
            else:
                name_string = f"{entity.from_user.first_name}"

            user_mentionable = f"<a href='tg://user?id={entity.from_user.id}'>{name_string}</a>"

        return user_mentionable
