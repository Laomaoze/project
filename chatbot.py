## chatbot.py
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
# The messageHandler is used for all message updates
import configparser
import logging
import json
import requests


def main():
    # Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("search", search_command))
    dispatcher.add_handler(CommandHandler("cal", calculate_command))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def search_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Where do you want to go?(please input the(keyword city)(关键词 城市) in the command prompt)')
    keywords = input("please input the keyword city(关键词+城市)\n")
    MapPlace().run(keywords)

def calculate_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    types = context.args[0]
    time = float(context.args[1])
    if types == "yoga":
        calories = time*300
    elif types == "treadmill":
        calories = time*350
    elif types == "swimming":
        calories = time*700
    elif types == "bicycle":
        calories = time*260
    elif types == "skating":
        calories = time*460
    elif types == "running":
        calories = time*650
    elif types == "skipping":
        calories = time*350
    elif types == "skateboard":
        calories = time*550
    elif types == "golf":
        calories = time*350
    elif types == "volleyball":
        calories = time*500
    else:
        update.message.reply_text('The sport is not recorded ')
        return
    calories = str(calories)
    update.message.reply_text('The calories are ' + calories)

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('If you type /search, you will find the location by the keyword and city in the command prompt.\n'
                              'if you type /cal sports time(h), it will calculate the calories for you.')


class MapPlace(object):
    def __init__(self):
        self.url = "https://restapi.amap.com/v3/place/text"
        self.key = "22599bfaf4e0a6860ebea23fc5dda171"
        self.keywords = ""
        self.city = ""

    def get_data(self):
        data = {"keywords": self.keywords, "key": self.key, "extensions": "base", "output": "json", "city": self.city}
        res = requests.get(self.url, data).json()
        return res

    @staticmethod
    def print_msg(res):
        cnt = 1
        for _res in res:
            print("********************{0}.rows********************".format(cnt))
            print("pname: %s" % _res[0])
            print("cityname: %s" % _res[1])
            print("type: %s" % _res[2])
            print("adname: %s" % _res[3])
            print("name: %s" % _res[4])
            print("location: %s" % _res[5])
            cnt += 1

    # https://restapi.amap.com/v3/place/text
    def del_place(self, res):
        data = []
        # print(json.dumps(res, ensure_ascii=False))
        if res["status"] != '1':
            print("Sorry {0} 关键词搜寻获取ERROR!!!".format(self.keywords))
            return
        else:
            for _res in res["pois"]:
                data.append([_res["pname"], _res["cityname"], _res["type"], _res["adname"], _res["name"], _res["location"]])
            return data

    def run(self, *args):
        cname = args[0].split()
        self.keywords = cname[0]
        if len(cname) > 1:
            self.city = cname[1]
        res = self.get_data()
        data = self.del_place(res)
        self.print_msg(data)
if __name__ == '__main__':
    main()
