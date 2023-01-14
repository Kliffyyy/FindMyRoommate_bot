import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler, ConversationHandler, MessageHandler,
    filters
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

GENDER, SLEEPTIME, SOCIALIZATION = range(3)


'''
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lastName = user.last_name if user.last_name is not None else ''
    firstName = user.first_name + ' ' if user.first_name is not None else ''
    reply_keyboard = [["Boy", "Girl", "Other"]]
    await update.message.reply_text(
        rf"Hi {lastName}{firstName}, welcome to FindMyRoomie! Let's get started with a few questions.",
        parse_mode='HTML'
    )
    await update.message.reply_text(
        "Please select your gender.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Male or Female?"
        )
    )

    return GENDER
'''

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stores the selected gender and asks for user's sleep time."""
    user = update.message.from_user
    lastName = user.last_name if user.last_name is not None else ''
    firstName = user.first_name + ' ' if user.first_name is not None else ''
    logger.info("gender of %s%s: %s", firstName, lastName, update.message.text)
    reply_keyboard = [["before 10pm", "10pm - 11pm", "11pm - 12pm", "12pm - 1am", "1am - 2am", "after 2am"]]
    await update.message.reply_text(
        "I see! Please tell me your usual sleep time.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True  
        )
    )

    return SLEEPTIME

async def sleeptime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stores the user's sleep time and asks for user's socialization preference."""
    user = update.message.from_user
    lastName = user.last_name if user.last_name is not None else ''
    firstName = user.first_name + ' ' if user.first_name is not None else ''
    logger.info("Sleep time of %s%s: %s", firstName, lastName, update.message.text)
    reply_keyboard = [["I want to stay alone", "quieter environment", "no preference", "more vibrant environment", "party all night long"]]
    await update.message.reply_text(
        "I see! Please tell me your socialization preference.",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True  
        )
    )

    return SOCIALIZATION

async def socialization(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stores the user's socialization preference and stops the conversation."""
    user = update.message.from_user
    lastName = user.last_name if user.last_name is not None else ''
    firstName = user.first_name + ' ' if user.first_name is not None else ''
    logger.info("Socialization preference of %s%s: %s", firstName, lastName, update.message.text)
    await update.message.reply_text("Thank you! Finding an available match...")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    lastName = user.last_name if user.last_name is not None else ''
    firstName = user.first_name + ' ' if user.first_name is not None else ''
    logger.info("User %s%s canceled the conversation.", firstName, lastName)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=
        "/start - Start the bot\n"
        "/help - Get help\n"
        "/echo - Echo the message"
    )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main():
    application = ApplicationBuilder().token(
        '5895820554:AAHRLbBdv-zymxreD1FY53uUj0ocjkP5-6g').build()

    help_handler = CommandHandler('help', help)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GENDER: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), gender)],
            SLEEPTIME: [MessageHandler(filters.Regex("^(before 10pm|10pm - 11pm|11pm - 12pm|12pm - 1am|1am - 2am|after 2am)$"), sleeptime)],
            SOCIALIZATION: [MessageHandler(filters.Regex("^(I want to stay alone|quieter environment|no preference|more vibrant environment|party all night long)$"), socialization)]
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(help_handler)
    application.add_handler(conv_handler)
    application.add_handler(unknown_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
