from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import *
import Constants as keys
import responses as R
import time


print("Bot started...")

GENDER, FACULTY, SLEEPING_HOURS = range(3)

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Type something random to get started') 

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('If you need help, you are in the wrong place...')

async def match_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Please fill in the survey below to tell us what type of roommates suits you the best! You may also type /quit to quit the conversation!")
    time.sleep(1)
    reply_keyboard = [["Male", "Female", "Others"]]
    await update.message.reply_text("Question 1: What is your gender? Available options: Male, Female, Others", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder="What is your gender?"), )
    return GENDER

async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:   
    user = update.message.from_user
    await update.message.reply_text("Noted on your gender, " + user.first_name + ".", reply_markup=ReplyKeyboardRemove(), )
    time.sleep(1)
    reply_keyboard = [["CHS", "Business", "Computing", "Dentistry", "CDE", "Law", "Medicine", "Nursing", "Pharmacy", "NUS College", "Music"]]
    await update.message.reply_text("Question 2: What is your faculty? Available options: CHS, Business, Computing, Dentistry, CDE, Law, Medicine, Nursing, Pharmacy, NUS College, Music", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder="What is your faculty?"), )
    return FACULTY 

async def faculty(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text("Noted on your faculty, " + user.first_name + ".", reply_markup=ReplyKeyboardRemove(), )
    time.sleep(1)
    reply_keyboard = [["before 9pm", "9-10pm", "10-11pm", "11-12am", "12-1am", "1-2am", "after 2am"]]
    await update.message.reply_text("Question 3: What are your sleeping hours? Available options: before 9pm, 9-10pm, 10-11pm, 11-12am, 12-1am, 1-2am, after 2am", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, input_field_placeholder="What are your sleeping hours?"), )
    return SLEEPING_HOURS

async def sleeping_hours(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    await update.message.reply_text("Noted on your sleeping hours, " + user.first_name + ". Thank you for filling up the survey. Your response has been recorded.", reply_markup=ReplyKeyboardRemove(), )
    return ConversationHandler.END

async def wrong_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("'%s' is an invalid command." % update.message.text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower()
    response = R.sample_responses(str(text))

    await update.message.reply_text(response)

async def end_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    return ConversationHandler.END

async def quit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    await update.message.reply_text("User quitted the conversation.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Update {update} caused error {context.error}")

def main():
    app = Application.builder().token(keys.API_KEY).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("match", match_command)], 
        states={
            GENDER: [MessageHandler(filters.Regex("^(Male|Female|Others)$"), gender)],
            FACULTY: [MessageHandler(filters.Regex("^(CHS|Business|Computing|Dentistry|CDE|Law|Medicine|Nursing|Pharmacy|NUS College|Music)$"), faculty)],
            SLEEPING_HOURS: [MessageHandler(filters.Regex("^(before 9pm|9-10pm|10-11pm|11-12am|12-1am|1-2am|after 2am)$"), sleeping_hours)],
        }, 
        fallbacks=[CommandHandler("quit", quit)])
    
    # commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("hello", hello))
    #app.add_handler(CommandHandler("match", match_command))
    app.add_handler(conv_handler)

    app.add_handler(MessageHandler(filters.COMMAND, wrong_command))
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    app.run_polling(1.0)

main()
