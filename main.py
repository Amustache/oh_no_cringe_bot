#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.
import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

# Enable logging
from secret import TOKEN
from videos import VIDEOS

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('This bot is inline, use @oh_no_cringe_bot to select a video.')


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('This bot is inline, use @oh_no_cringe_bot to select a video.')


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    query = update.inline_query.query

    if query != "":
        videos_search = [(title, url_id) for title, url_id in VIDEOS if query.lower() in title.lower()]
    else:
        videos_search = VIDEOS

    results = [
        InlineQueryResultArticle(
            id=str(f"vide_{uuid4()}"),
            title=f"{title}",
            input_message_content=InputTextMessageContent(f"https://youtu.be/{url_id}"),
            thumb_url=f"https://img.youtube.com/vi/{url_id}/default.jpg",
        )
        for title, url_id in videos_search
    ]

    update.inline_query.answer(results)


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(InlineQueryHandler(inlinequery))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
