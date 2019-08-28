#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import (MessageHandler, Filters)
import random

import config

# enable logging
logFormat = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=logFormat, level=logging.DEBUG)
logger = logging.getLogger(__name__)

#############################
#         functions         #
#############################


def get_full_name(update):
    return update.message.from_user.first_name + " " + update.message.from_user.last_name


def get_username(update):
    return update.message.from_user.username


def get_greeting():
    return random.choice([
        "C'e sempre un motivo per iniziare bene la giornata: un sorriso, un po' di ottimismo, l'importante è iniziare. Il motivo certamente arriverà, anche dopo un buon caffè...Buongiorno."
    ])

#############################
#         commands          #
#############################


def start(bot, update):
    chat_id = update.message.chat_id
    logger.debug('[%s] start command received' % (chat_id))
    bot.send_message(chat_id=chat_id, text="c_bot is under aggressive development")


def read(bot, update):
    chat_id = update.message.chat_id
    logger.debug('[%s] read a message from chat' % (chat_id))
    username = get_username(update)
    logger.debug('[%s] sender is "%s"' % (chat_id, username))
    bot.send_message(chat_id=chat_id, text=get_greeting())

def error(bot, update, error):
    logger.error('Update "%s" caused error "%s"' % (update, error))

#############################
#           main            #
#############################


def main():
    try:
        config.read_config('settings.json')
        telegram_key = config.get_telegram_key()
    except FileNotFoundError as e:
        logger.warn('No configuration file found, fallback to env variable for API key. Cause: %s' % (e))
        telegram_key = os.environ.get('TELEGRAM_API_KEY')
        if telegram_key is None:
           raise ValueError('TELEGRAM_API_KEY variable not set')

    updater = Updater(token=telegram_key)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands
    dispatcher.add_handler(CommandHandler('start', start))

    # on noncommand i.e message - do something
    dispatcher.add_handler(MessageHandler(Filters.text, read))

    # log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT.
    updater.idle()


if __name__ == '__main__':
    main()
