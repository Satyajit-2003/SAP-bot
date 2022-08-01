import os

class configurations():
    def __init__(self):
        # Configure your environment here
        self.USERNAME = '' or os.environ.get("USERNAME")
        self.PASSWORD = '' or os.environ.get("PASSWORD")
        self.TELEGRAM_BOT_API = '' or os.environ.get("TELEGRAM_BOT_API")
        self.TELEGRAM_CHAT_ID = '' or os.environ.get("TELEGRAM_CHAT_ID")


        #DO NOT EDIT BELOW THIS CONFIGURATION
        self.CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH")
        self.GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN")

CONFIG = configurations()

