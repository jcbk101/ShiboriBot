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

import Advisory
import Constants as Keys
import Responses as Res
import logging
from timeit import default_timer as timer

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
Keys.BOT_KEY = os.environ[ "BOT_ID" ]
Keys.BSC_KEY = os.environ[ "BSC_ID" ]
Keys.CHAT_ID = os.environ[ "SNT_ID" ]
Keys.TEST_ID = os.environ[ "TEST_ID" ]
Keys.CMC_KEY = os.environ[ "CMC_ID" ]
Keys.SNT_CONTRACT = os.environ[ "SNT_CONTRACT" ]
Keys.SNT_BURNED = os.environ[ "SNT_BURNED" ]
Keys.SNT_MARKETING = os.environ[ "SNT_MARKETING" ]
Keys.SNT_TOURNAMENT = os.environ[ "TEST_TOURNAMENT" ]
Keys.SNT_DEVELOPER = os.environ[ "SNT_DEV" ]


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
# Re-enable messages
#
# ------------------------------------------
def message_queue(context):
    global global_msg_test
    global global_msg_count
    global global_timer

    global_msg_test = False
    global_msg_count = 0
    global_timer = timer()
    return


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
# Error handler
#
# ------------------------------------------
def error(update, context):
    print(f"Update {update}\n caused an error: {context.error}")


# ------------------------------------------
#
# Start auto warning updates
#
# ------------------------------------------
def advisor_start(update, context):
    chat_id = update.message.chat_id
    user_id = update.effective_user.id
    global notAdmin

    # Check for Admins
    admins = update.effective_user.bot.get_chat_member(chat_id, user_id)
    if admins and admins.status in [ 'creator', 'administrator' ]:
        # if context.job_queue.scheduler.running:
        #    context.job_queue.start()
        # else:
        context.job_queue.run_repeating(Advisory.get_reminder_msg, 1800, context = chat_id)
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
# Stop auto warning updates
#
# ------------------------------------------
def advisory_stop(update, context):
    global notAdmin

    if context.job_queue.scheduler.running:
        chat_id = update.message.chat_id
        bot = update.effective_user.bot
        user_id = update.effective_user.id

        # Check for Admins
        admins = update.effective_user.bot.get_chat_member(chat_id, user_id)
        if admins and admins.status in [ 'creator', 'administrator' ]:
            # bot.send_message(chat_id = chat_id, text = 'Stopped!')
            # context.job_queue.stop()
            current_jobs = context.job_queue.jobs()
            if current_jobs:
                for job in current_jobs:
                    job.schedule_removal()
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
# Used only for 'notAdmin' list management
#
# ------------------------------------------
def clear_members(context):
    global notAdmin
    notAdmin.clear()
    return
    """    was_member, is_member = True
        cause_name = update.chat_member.from_user.mention_html()
        member_name = update.chat_member.new_chat_member.user.mention_html()

        if not was_member and is_member:
            update.effective_chat.send_message(
                f"{member_name} was added by {cause_name}. Welcome!",
                parse_mode = ParseMode.HTML,
            )
        elif was_member and not is_member:
            update.effective_chat.send_message(
                f"{member_name} is no longer with us. Thanks a lot, {cause_name} ...",
                parse_mode = ParseMode.HTML,
            )
    """


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
    # Auto message handler: Warnings, broadcast
    # --------------------------------------------
    dp.add_handler(CommandHandler('advise_on', advisor_start))
    dp.add_handler(CommandHandler('advise_off', advisory_stop))

    # --------------------------------------------
    # Default messages handler
    # --------------------------------------------
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Handle members joining/leaving chats.
    # dp.add_handler(ChatMemberHandler(clear_members, ChatMemberHandler.CHAT_MEMBER))

    # --------------------------------------------
    # Error handler
    # --------------------------------------------
    dp.add_error_handler(error)

    # Start the warnings now!
    job.run_repeating(Advisory.get_reminder_msg, 1800, context = Keys.TEST_ID)

    # Clear member IDs who try and chat to the bot directly!
    job.run_daily(clear_members,
                  datetime.time(hour = 7, minute = 00, tzinfo = pytz.timezone('US/Eastern')),
                  days = (0, 1, 2, 3, 4, 5, 6),
                  context = Keys.CHAT_ID
                  )

    # updater.start_polling(allowed_updates = Update.ALL_TYPES)
    updater.start_webhook(listen = "0.0.0.0",
                          port = int(PORT),
                          url_path = Keys.BOT_KEY)
    updater.bot.setWebhook('https://your-app-name.herokuapp.com/' + Keys.BOT_KEY)
    updater.idle()


if __name__ == '__main__':
    main()
