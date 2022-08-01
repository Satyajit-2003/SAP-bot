from apscheduler.schedulers.blocking import BlockingScheduler
from main import extract_data, send_details

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=6)
def timed_job():
    print('This job is runs every siz hours and send attendance by Telegram Bot')
    extract_data()
    send_details()


sched.start()