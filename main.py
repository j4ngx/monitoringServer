#!/usr/bin/env python3
"""
This a bot telegram to monitoring a server
"""

import logging
import os
import subprocess
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

options = {"restart": "rebooting", "start": "starting", "stop": "stoping"}

#systemctl status ssh | grep active | cut -d":" -f 2 | cut -d" " -f 2,3
# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def monitoring_command(update: Update, context:CallbackContext):
    if str(update.message.chat_id) == '#ID_USER':
            command = update.message.text
            service = command.split(" ")[1]
            option = command.split("/")[1].split(" ")[0]

            if option == "status":
                os.system("systemctl status "+service+" | grep active | cut -d\":\" -f 2 | cut -d\" \" -f 2,3 > tmp.txt")
                status = open('tmp.txt', 'r').read()
                    
                if status != "":
                    update.message.reply_text('Status service "'+service+'": ')
                    update.message.reply_text(status)
                else:
                    update.message.reply_text('The service '+service+' is not installed')

                os.system("rm tmp.txt")

            else:
                for aux_option in options:
                    if aux_option == option:
                        os.system("systemctl "+option+" "+service)
                        update.message.reply_text("The servive "+service+" is "+options[option])
        
    else:
        update.message.reply_text('Invalid user')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start_bot", start))
    dispatcher.add_handler(CommandHandler("status",monitoring_command))
    dispatcher.add_handler(CommandHandler("restart",monitoring_command))
    dispatcher.add_handler(CommandHandler("start",monitoring_command))
    dispatcher.add_handler(CommandHandler("stop",monitoring_command))


    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
