import src
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
import logging

import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))
from daemon import Daemon
import config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


class Bot(Daemon):
    data = config.get_bot_data()

    def run(self):
        # Create the EventHandler and pass it your bot's token.
        self.updater = Updater(Bot.data["token"])

        # Get the dispatcher to register handlers
        self.dp = self.updater.dispatcher

        # on different commands - answer in Telegram
        self.dp.addHandler(CommandHandler("start", Bot.start_bot))
        self.dp.addHandler(CommandHandler("help", Bot.help))

        # on noncommand i.e message - echo the message on Telegram
        self.dp.addHandler(MessageHandler([Filters.text], Bot.answer_text))
        self.dp.addHandler(MessageHandler([Filters.sticker], Bot.answer_to_sticker))

        # log all errors
        self.dp.addErrorHandler(Bot.error)

        # Start the Bot
        self.updater.start_polling()

        # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        self.updater.idle()

    # Define a few command handlers. These usually take the two arguments bot and
    # update. Error handlers also receive the raised TelegramError object in error.
    @staticmethod
    def start_bot(bot, update):
        bot.sendMessage(update.message.chat_id, text='Hi! Please, enter the password to preceed.')

    @staticmethod
    def help(bot, update):
        bot.sendMessage(update.message.chat_id, text='Help!')

    @staticmethod
    def echo(bot, update):
        bot.sendMessage(update.message.chat_id, text=update.message.text)

    @staticmethod
    def answer_text(bot, update):
        if update.message.chat_id not in Bot.data["white_list"]:
            if update.message.text == Bot.data["password"]:
                logger.debug("Newcomer with the right password: id=%s", update.message.chat_id)
                Bot.data["white_list"].append(update.message.chat_id)
                logger.debug("New whitelist: %s", Bot.data["white_list"])
                config.update(config.BOT, Bot.data)
                bot.sendMessage(chat_id=update.message.chat_id, text="Welcome! Nice to meet you :)")
            else:
                bot.sendMessage(chat_id=update.message.chat_id, text="Sorry, the password is incorrect.")
        else:
            Bot.answer_the_question(bot, update)

    @staticmethod
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

    @staticmethod
    def answer_to_sticker(bot, update):
        bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
        bot.sendSticker(chat_id=update.message.chat_id, sticker=update.message.sticker.file_id)
        response = "I love you too, Sweetheart ;) Your sticker file_id is " + update.message.sticker.file_id
        bot.sendMessage(chat_id=update.message.chat_id, text=response)

    @staticmethod
    def error(bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))
