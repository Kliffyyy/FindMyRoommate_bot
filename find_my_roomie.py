import logging
from telegram import Update
from telegram.ext import *
import Constants as key
import data as d

# variables
question_counter = 0

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text= (d.start) + "\n...If I am not wrong your name is " + f"{update.effective_user.full_name}...")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global question_counter 
    await context.bot.send_message(chat_id=update.effective_chat.id, text= d.qn[question_counter])
    print((update.message.text).lower(), update.message.id, update.message.date, update.effective_message.chat_id) # for the backend
    question_counter += 1
'''
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)
'''
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(key.API_KEY).build()
    
    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    # caps_handler = CommandHandler('caps', caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    # application.add_handler(caps_handler)
    application.add_handler(unknown_handler)
    
    
    application.run_polling()