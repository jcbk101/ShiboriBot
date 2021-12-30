#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import datetime

import Constants as Keys
import logging

import pytz
from telegram.ext import *
from telegram import Update
import os

logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)

# Restrictions
global_msg_test = False
global_msg_count = 0
global_timer = timer()
notAdmin = [ ]

# YEP, SECRETS!
PORT = int(os.environ.get('PORT', 5000))



# ------------------------------------------
#
# BOT start command
#
# ------------------------------------------
def start_command(update, context):
    chat_id = update.message.chat_id
    user_id = update.effective_user.id

    # Check for Admins
    admins = update.effective_user.bot.get_chat_member(chat_id, user_id)
    if admins and admins.status in [ 'creator', 'administrator' ]:
        advisor_start(update, context)
    else:
        update.message.reply_text("Admin only command")


def help_command(update, context):
    user = update.effective_user
    update.message.reply_text('Have you tried Google?')




# ------------------------------------------
#
# Process user request
#
# ------------------------------------------
def handle_message(update, context):
    global global_msg_test
    global global_msg_count
    global global_timer
    global notAdmin
    chat_id = update.message.chat_id
    user_id = update.effective_user.id

    # Only works in Test Group and Shibori Clan Group
    if chat_id == Keys.CHAT_ID or chat_id == Keys.TEST_ID:

        if global_msg_test:
            return
        #
        text = str(update.message.text).lower()
        response = Res.sample_responses(text, update)
        #    update.message.reply_text(response, parse_mode='Html')

        if response:
            update.message.reply_text(response, parse_mode = 'Html')

        # Set flag to pause messages for a bit
        global_msg_count += 1
        new_time = timer()
        if global_msg_count >= 4 and (new_time - global_timer) < 2:
            global_msg_test = True
            context.job_queue.run_once(message_queue, 5, context = chat_id)
        else:
            global_timer = timer()
    else:
        # Restrict private messaging
        # save the user for a little
        if user_id not in notAdmin:
            update.message.reply_text("I don't respond here")
            notAdmin.append(user_id)
            notAdmin = list(set(notAdmin))
        return


# ------------------------------------------
#
# Error handler.
#
# ------------------------------------------
def error(update, context):
    print(f"Update {update}\n caused an error: {context.error}")



# ------------------------------------------
#
# Main
#
# ------------------------------------------
def main():
    updater = Updater(Keys.BOT_KEY, use_context = True)
    dp = updater.dispatcher
    job = updater.job_queue

    # --------------------------------------------
    # Basic Command handlers
    # --------------------------------------------
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('restart_start', start_command))
    dp.add_handler(CommandHandler('help', help_command))

    # --------------------------------------------
    # Default messages handler
    # --------------------------------------------
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # --------------------------------------------
    # Error handler
    # --------------------------------------------
    dp.add_error_handler(error)


    # updater.start_polling(allowed_updates = Update.ALL_TYPES)
    updater.start_webhook(listen = "0.0.0.0",
                          port = int(PORT),
                          url_path = Keys.BOT_KEY)
    updater.bot.setWebhook('https://shibori-bot.herokuapp.com/' + Keys.BOT_KEY)
    updater.idle()


if __name__ == '__main__':
    main()
