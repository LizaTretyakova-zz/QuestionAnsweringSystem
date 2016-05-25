#!/usr/bin/env python3

import src
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import config

logger = config.get_logger()
data = config.get_bot_data()


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def help(bot, update):
    bot.sendMessage(update.message.chat_id, text='Help!')


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def answer_text(bot, update):
    if update.message.chat_id not in data["white_list"]:
        if update.message.text == data["password"]:
            # print("Newcomer with the right password: id=%s", update.message.chat_id)
            logger.debug("Newcomer with the right password: id=%s", update.message.chat_id)
            data["white_list"].append(update.message.chat_id)
            # print("New whitelist: %s", data["white_list"])
            logger.debug("New whitelist: %s", data["white_list"])
            config.update(config.BOT, data)
            bot.sendMessage(chat_id=update.message.chat_id, text="Welcome! Nice to meet you :)")
        else:
            bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, the password is incorrect.")
    else:
        answer_the_question(bot, update)


def answer_the_question(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    answer = src.process_question(update.message.text)
    if answer:
        bot.sendMessage(chat_id=update.message.chat_id, text=answer)
    else:
        bot.sendSticker(chat_id=update.message.chat_id, sticker="BQADAgADUAAD-Aq8AhYQmf3YFjltAg")
        bot.sendMessage(chat_id=update.message.chat_id,
                        text="With all due respect we have not got your question." +
                             "Would you please mind repeating it with some more precise information?")


def answer_to_sticker(bot, update):
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    bot.sendSticker(chat_id=update.message.chat_id, sticker=update.message.sticker.file_id)
    response = "I love you too, Sweetheart ;) Your sticker file_id is " + update.message.sticker.file_id
    bot.sendMessage(chat_id=update.message.chat_id, text=response)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def run_bot():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(data["token"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.addHandler(CommandHandler("start", start))
    dp.addHandler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.addHandler(MessageHandler([Filters.text], answer_text))
    dp.addHandler(MessageHandler([Filters.sticker], answer_to_sticker))

    # log all errors
    dp.addErrorHandler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    # src.run()
    run_bot()
