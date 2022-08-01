from apscheduler.schedulers.blocking import BlockingScheduler
from main import extract_data, send_details
from config import CONFIG

sched = BlockingScheduler()

@sched.scheduled_job('interval', hours=int(CONFIG.TIME_INTERVAL))
def timed_job():
    print(f'This job is runs every {CONFIG.TIME_INTERVAL} hours and send attendance by Telegram Bot')
    extract_data()
    send_details()


sched.start()