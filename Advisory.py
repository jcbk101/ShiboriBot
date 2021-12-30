def get_reminder_msg(context):
    reminder = "⚠<b><u>REMINDER</u></b>⚠\n" \
               "\n" \
               "There is NO 'Shib Ninja Dojo: Clan Shibori Support'.\n" \
               "$SNT does not have '<b>Support Desk</b>', '<b>Help Desk</b>'\n" \
               "nor will any TEAM or MODS DM you first.\n" \
               "\n" \
               "If anyone should send you a DM, and says they are a\n" \
               "team member, IE: Admin, Dev, MOD, official Support\n" \
               "or Help person, it is more than likely a scam\n" \
               "attempt and you should ignore them and block immediately!"

    warning = "🚨<b><u>Please Be aware!</u></b>🚨\n" \
              "\n" \
              "Sacmmers will do what ever the can to steal your\n" \
              "crypto from you. A loss of all funds could be\n" \
              "devastating. Be sure to do everything in your power\n" \
              "to protect what is yours!\n" \
              "\n" \
              "🥷<b><u>Helpful Tips:</u></b>🥷\n" \
              "Update your security settings to prevent you from being\n" \
              "added to potentially harmful telegram groups. That action\n" \
              "could lead to your crypto being put at risk of theft!\n" \
              "If your funds are stolen, there is no way you can get\n" \
              "it back.\n" \
              "To change your settings, do the following: \n" \
              "Go to <b>Settings</b>, then <b>Privacy and Security</b>\n" \
              "and make the neccessary changes.\n" \
              " \n" \
              "If you have any questions, you should DM our staff\n" \
              "yourself. Get to know us so that there is no confusion.\n" \
              "No one in the Shibori Clan will DM you first. Protect\n" \
              "all of your secret keys, seed phrases, and recovery keys\n" \
              "to your wallet(s). Only use the SNT contract addresses \n" \
              "posted here by our staff members, our <b>OFFICIAL</b> bot(s)\n" \
              "or on our <b>OFFICIAL</b> social media channels.\n" \
              "All admin will have a title to the right of their name\n" \
              "when messaging in the group.\n" \
              "\n   - Shibori Clan Dojo Staff"

    context.bot.send_message(context.job.context, text = reminder, parse_mode = 'Html')
    context.bot.send_message(context.job.context, text = warning, parse_mode = 'Html')
    return
