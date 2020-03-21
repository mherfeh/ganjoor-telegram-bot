#!/bin/python3

import logging
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from poets_glossary import poets_name_glossary


# Logging 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# Start button command
def start(update, context):
    chatID = update.effective_chat.id
    welcome = ' کافیه اسم شاعر مورد نظرت رو بنویس تا بیت شعری ازش تقدیم کنیم'
    commands = 'دستور /commands بهت کمک می‌کنه تا لیست دستورات موجود رو ببینی'
    context.bot.send_message(chat_id=chatID, text=welcome+'\n'+commands)

def about(update, context):
    chatID = update.effective_chat.id
    url = 'https://github.com/nelforza/ganjoor-telegram-bot'
    text = '''
    این ربات توسط حسین حیدری و به زبان پایتون نوشته شده و تحت لایسنس آزاد GPL منتشر شده است.


اگر ایده‌ای دارید که بشه بهش اضافه کرد: @addones
لینک به ریپو گیت‌هاب:
    '''
    context.bot.send_message(chat_id=chatID, text=text+'\n'+url)

def commands(update, context):
    chatID = update.effective_chat.id
    text = '''ریپو کد:
/about
متن شروع:
/start
لیست شاعران:
/poets
برای همین پیام که الان می‌بینید :)
/commands'''
    context.bot.send_message(chat_id=chatID, text=text)

def poets(update, context):
    chatID = update.effective_chat.id
    poets = ''
    for value in poets_name_glossary.values():
        poets += str(value)+'\n'
    context.bot.send_message(chat_id=chatID, text=poets)




def poem(update, context):
    chatID = update.effective_chat.id
    text = 'شاعری با این اسم پیدا نشد!'
    msg = update.message.text
    if msg not in poets_name_glossary.values():
        context.bot.send_message(chat_id=chatID, text=text)



def main():
    ####  Starting the bot ####

    # creates Updater and passes TOKEN
    updater = Updater(token='Token', use_context=True)
    
    # Getting dispatcher to register handlers
    dp = updater.dispatcher

    # Registering my functions
    start_handler = CommandHandler('start', start)
    poets_handler = CommandHandler('poets', poets)
    about_handler = CommandHandler('about', about)
    command_handler = CommandHandler('commands', commands)
    msg_handler = MessageHandler(Filters.text, poem)

    dp.add_handler(start_handler)
    dp.add_handler(poets_handler)
    dp.add_handler(about_handler)
    dp.add_handler(command_handler)
    dp.add_handler(msg_handler)


    # Registering Error fuctions
    dp.add_error_handler(error)
    
    # Starts BOT
    updater.start_polling()

    # Keep it active untile CTRL + C
    updater.idle()

if __name__ == "__main__":
    main()