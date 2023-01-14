from telegram import Update
from telegram.ext import *
import Constants as keys
import responses as R

print("Bot started...")

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Type something random to get started') 

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('If you need help, you are in the wrong place...')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (update.message)
    # print(type(text))
    print(str(text))
    response = R.sample_responses(str(text))

    await update.message.reply_text(response)

def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Update {update} caused error {context.error}")

def main():
    app = Application.builder().token(keys.API_KEY).build()
    
    # commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("hello", hello))

    app.add_handler(MessageHandler(filters.COMMAND, handle_message))

    app.add_error_handler(error)
    app.run_polling(0)

main()
