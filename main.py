from telegram import Update
from telegram.ext import *
import Constants as key
from datetime import datetime
import data as d

print("Bot started...")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Type something random to get started') 

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/hello for some greetings"
        "/start to start answering questions"
        "/help is this exact help page"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global question_counter 
    await context.bot.send_message(chat_id=update.effective_chat.id, text= d.qn[question_counter])
    print((update.message.text).lower(), update.message.id, update.message.date, update.effective_message.chat_id) # for the backend
    question_counter += 1

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.message)
    # print(type(text))
    print(str(text))
    response = sample_responses(str(text))

    await update.message.reply_text(response)

def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Update {update} caused error {context.error}")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def sample_responses(input_text):
    user_message = str(input_text)
    print(user_message)

    if user_message in ("hello", "hi", "sup"):
        return "Hey! How's it going?" 

    elif user_message in ("who are you", "who are you?"):
        return "I am a bot to match you to a roomate that you will benefit from."
    
    elif user_message in ("sleep"):
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        return str("Goodnight! It is currently " + date_time)
    
    #elif user_message in ("answer questions"):
        

    else:
        return "I do not understand you."

if __name__ == '__main__':
    application = ApplicationBuilder().token(key.API_KEY).build()
    
    start_handler = CommandHandler('start', start_command)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    # caps_handler = CommandHandler('caps', caps)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    
    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    # application.add_handler(caps_handler)
    application.add_handler(unknown_handler)
    
    
    application.run_polling()
