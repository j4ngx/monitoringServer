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

options = ("restart" : "rebooting", "start" : "starting", "stop" : "stoping")

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

def getOption():
	print(command.split("/")[1].split(" ")[0])

def status_command(update: Update, context:CallbackContext):
	if str(update.message.chat_id) == '576384241':
            command=update.message.text
            service=command.split(" ")[1]
            
            os.system("systemctl status "+service+" | grep active | cut -d\":\" -f 2 | cut -d\" \" -f 2,3 > tmp")
            status = open('tmp', 'r').read()
                
            if status != "":
                update.message.reply_text('Status service "'+service+'": ')
                update.message.reply_text(status)
            else:
                update.message.reply_text('The service '+service+' is not installed')

            os.system("rm tmp")
	else:
		update.message.reply_text('Invalid user')

def monitoring_command(update: Update, context:CallbackContext):
	if str(update.message.chat_id) == '576384241':
            command = update.message.text
            service = command.split(" ")[1]
	    option = command.split("/")[1].split(" ")[0]
            
            os.system("systemctl "+option+" "+service)
	
            for aux_option in options:
		if aux_option == option:
	    	    update.message.reply_text("The servive "+service+"is "+option)
		
	else:
		update.message.reply_text('Invalid user')

def start_command(update: Update, context:CallbackContext):
	if str(update.message.chat_id) == '576384241':
            command=update.message.text
            service=command.split(" ")[1]
            
            os.system("systemctl start "+service)
           
	    update.message.reply_text("The servive "+service+"is starting")
	else:
		update.message.reply_text('Invalid user')

def stop_command(update: Update, context:CallbackContext):
	if str(update.message.chat_id) == '576384241':
            command=update.message.text
            service=command.split(" ")[1]
            
            os.system("systemctl stop "+service)
           
	    update.message.reply_text("The servive "+service+"is stoping")
	else:
		update.message.reply_text('Invalid user')

		
def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5229043461:AAGNWtnlqMHrNBIkkVuUOwBBDA3T7B6HIHY")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("status",status_command))
    dispatcher.add_handler(CommandHandler("restart",restart_command))
    dispatcher.add_handler(CommandHandler("start",start_command))
    dispatcher.add_handler(CommandHandler("stop",stop_command))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
