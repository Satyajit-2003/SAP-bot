import os

class configurations():
    def __init__(self):
        # Configure your environment here
        # pass values inside the quotes
        # For multiple vales (where applicable), pass the values as comma separated values

        # SAP DETAILS
        self.USERNAME = '' or os.environ.get("USERNAME")
        self.PASSWORD = '' or os.environ.get("PASSWORD")
        self.SESSION = '' or os.environ.get("SESSION")     #Pass as 20XX-20XX
        self.SEMESTER = '' or os.environ.get("SEMESTER")   #Pass as 'Autumn', 'Spring' or any other semester

        # TELEGRAM DETAILS
        self.TELEGRAM_BOT_API = '' or os.environ.get("TELEGRAM_BOT_API")
        self.TELEGRAM_CHAT_ID = '' or os.environ.get("TELEGRAM_CHAT_ID")

        # SCHEDULER DETAILS
        self.UPDATE_INTERVAL = '3' or os.environ.get("TIME_INTERVAL")  #In hours
        self.ATTENDANCE_TIME = '15:30, 3:30' or os.environ.get("ATTENDANCE_TIME")  #In 24 hour format
        self.WARNING_TIME = '15:30, 4:00' or os.environ.get("WARNING_TIME")  #In 24 hour format


        ###----DO NOT EDIT BELOW THIS CONFIGURATION---##
        self.CHROMEDRIVER_PATH = os.environ.get("CHROMEDRIVER_PATH") or '.\chromedriver.exe'
        self.GOOGLE_CHROME_BIN = os.environ.get("GOOGLE_CHROME_BIN") or r'C:\Program Files\Google\Chrome\Application\chrome.exe'

CONFIG = configurations()

