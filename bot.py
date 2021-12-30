#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.
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


# ------------------------------------------
#
# To be updated
#
# ------------------------------------------
def help_command(update, context):
    user = update.effective_user
    # update.message.reply_text('Have you tried Google? 🧐')
    helper = "The follow commands are supported:\n" \
             "\n" \
             "/buy - Info on how you can buy SNT\n" \
             "/mc - SNT Market CAP info\n" \
             "/ninja - SNT founder's twitter\n" \
             "/vote - Vote for Shib Ninja Token\n" \
             "/contract - Links to contracts\n" \
             "/rewards - Rewards details\n" \
             "/chart - Links to chart info\n" \
             "/twitter - Official Shibori Clan twitter\n" \
             "/website - Official Shib Ninja Token website\n" \
             "/reddit - Official reddit\n" \
             "/discord - Official discord\n" \
             "/social - SNT Official social media links\n" \
             "/info - General Shib Ninja Token info\n" \
             "/donate - Donate to the SNT project\n" \
             "/roadmap - SNT roadmap info\n"
    update.message.reply_text(helper)


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

    # ----------------------------------------
    # Only group chats!
    # ----------------------------------------
    if 'group' in update.message.chat.type:
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
# Start auto warning updates
#
# ------------------------------------------
def advisor_start(update, context):
    chat_id = update.message.chat_id
    user_id = update.effective_user.id
    job = context.job_queue.get_jobs_by_name('get_reminder_msg')
    global notAdmin

    # Check for Admins
    admins = update.effective_user.bot.get_chat_member(chat_id, user_id)
    if admins and admins.status in [ 'creator', 'administrator' ]:
        if not job:
            context.job_queue.run_repeating(Advisory.get_reminder_msg, 180, context = chat_id)
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
                    # Only delete this job: reminder messages
                    if job.name == 'get_reminder_msg':
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
    job.run_repeating(Advisory.get_reminder_msg, 180, context = Keys.TEST_ID)

    # Clear member IDs who try and chat to the bot directly!
    job.run_daily(clear_members,
                  datetime.time(hour = 7, minute = 00, tzinfo = pytz.timezone('US/Eastern')),
                  days = (0, 1, 2, 3, 4, 5, 6),
                  context = Keys.CHAT_ID
                  )

    # updater.start_polling(allowed_updates = Update.ALL_TYPES)
    updater.start_webhook(listen = "0.0.0.0",
                          port = int(PORT),
                          url_path = Keys.BOT_KEY,
                          webhook_url = "https://shibori-bot.herokuapp.com/" + Keys.BOT_KEY
                          )
    updater.idle()


if __name__ == '__main__':
    main()
