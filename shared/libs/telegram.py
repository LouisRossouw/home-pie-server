import os
import sys

import telebot

from django.conf import settings
from dotenv import load_dotenv

load_dotenv()


class BotNotification():
    """ Basic Notification class for Telebot. """

    def __init__(self):
        """ initialize. """

        BOT_TOKEN = os.getenv("TELEGRAM_BOT")
        TELEBOT_ADMIN_ALIAS = os.getenv("TELEBOT_ADMIN_ALIAS")

        self.notifications = True
        self.bot = telebot.TeleBot(BOT_TOKEN)
        self.ADMIN_ID = TELEBOT_ADMIN_ALIAS.split("-")[3]

    def send_ADMIN_notification(self, text):
        """ Send notification to Admin ID only. """

        try:
            if self.notifications == True:
                self.bot.send_message(chat_id=self.ADMIN_ID,
                                      allow_sending_without_reply=True, text=str(text))
        except Exception as e:
            print(e)


if __name__ == "__main__":

    BotNot = BotNotification()
    BotNot.send_ADMIN_notification("hello")
