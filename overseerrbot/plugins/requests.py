from io import BytesIO

from pyrogram import emoji
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from overseerrbot import OverseerrBot
from overseerrbot.api.OverseerrApi import OverseerrApi
from overseerrbot.helpers import filters
from overseerrbot.redis import RedisDatabase


async def get_media_poster(poster_path):
    """
    Determines the poster path and returns the poster.
    """
    api = OverseerrApi()

    poster_binary = await api.get_poster(poster_path)
    poster = BytesIO(poster_binary)

    if poster.getbuffer().nbytes < 0:
        # Overseerr logo as default image. Will change later.
        poster = 'https://raw.githubusercontent.com/sct/overseerr/68c7b3650ec82437bdb128f72f734e227ad763cb/public' \
                 '/apple-splash-2778-1284.jpg'

    return poster


async def make_request_buttons(request_id):
    """
    Makes the buttons for the request message.
    """
    buttons = [
        [
            InlineKeyboardButton(f"{emoji.CHECK_MARK_BUTTON} Approve Request",
                                 callback_data=f"approve_request+{request_id}"),
        ],
        [
            InlineKeyboardButton(f"{emoji.STOP_SIGN} Deny Request",
                                 callback_data=f"deny_request+{request_id}"),
        ]
    ]

    return buttons


@OverseerrBot.on_message(filters.command('requests'))
@OverseerrBot.admins_only
async def send_requests(_, message: Message):
    api = OverseerrApi()
    redis = RedisDatabase()
    new_requests_sent = False
    media_requests = await api.get_requests()

    for media_request in media_requests['results']:
        if media_request['status'] == 1:
            request_id = media_request['id']
            media_id = media_request['media']['tmdbId']
            media_type = media_request['type'].lower()

            if not redis.checkIfSent(media_request['id']):
                media_details = await api.get_media_details(media_type, media_id)
                poster = await get_media_poster(media_details['posterPath'])

                name = ''
                if 'name' in media_details:
                    name = media_details['name']
                elif 'title' in media_details:
                    name = media_details['title']

                message = await message.reply_photo(
                    photo=poster,
                    caption=(
                        f"{name} is pending approval.\n\n"
                        f"Requested By: {media_request['requestedBy']['displayName']}\n"
                    ),
                    reply_markup=InlineKeyboardMarkup(await make_request_buttons(request_id))
                )

                if message.id:
                    new_requests_sent = True
                    redis.markAsSent(media_request['id'])
            else:
                print('Already sent.')

    if not new_requests_sent:
        await message.reply('No new requests.')


@OverseerrBot.on_callback_query(filters.callback_query('approve_request'))
@OverseerrBot.admins_only
async def approve_request(bot: OverseerrBot, callback: CallbackQuery):
    request_id = callback.data.split('+')[1]
    api = OverseerrApi()
    try:
        await api.approve_request(int(request_id))
        await callback.message.edit_caption("This media request has been approved!")

    except Exception as e:
        print(e)
        await callback.answer("Error approving request.", show_alert=True)
        return

    await callback.answer("Request Approved")


@OverseerrBot.on_callback_query(filters.callback_query('deny_request'))
@OverseerrBot.admins_only
async def deny_request(bot: OverseerrBot, callback: CallbackQuery):
    request_id = callback.data.split('+')[1]
    api = OverseerrApi()
    try:
        await api.deny_request(int(request_id))
        await callback.message.edit_caption("This media request has been rejected!")

    except Exception as e:
        print(e)
        await callback.answer("Error rejecting request.", show_alert=True)
        return

    await callback.answer("Request Rejected")
