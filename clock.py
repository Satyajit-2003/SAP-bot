from apscheduler.schedulers.blocking import BlockingScheduler
from main import extract_data, send_details, send_warnings
from config import CONFIG
msg_sched = BlockingScheduler()
warn_sched = BlockingScheduler()

# @msg_sched.scheduled_job('interval', seconds=10)
@msg_sched.scheduled_job('interval', hours = int(CONFIG.TIME_INTERVAL))
def timed_job():
    print(f'This job is runs every {CONFIG.TIME_INTERVAL} hours and send attendance by Telegram Bot')
    user_list = CONFIG.USERNAME.split(',')
    pass_list = CONFIG.PASSWORD.split(',')
    chat_id_list = CONFIG.TELEGRAM_CHAT_ID.split(',')
    for i in range(len(user_list)):
        extract_data(user_list[i].strip(), pass_list[i].strip())
        send_details(user_list[i].strip(), chat_id_list[i].strip())

@warn_sched.scheduled_job('cron', hour='16', minute='30')
def scheduled_job():
    print("This job sends warning message to the user everyday at 4:30 PM GMT i.e. 10:00 PM IST")
    user_list = CONFIG.USERNAME.split(',')
    chat_id_list = CONFIG.TELEGRAM_CHAT_ID.split(',')
    for i in range(len(user_list)):
        send_warnings(user_list[i].strip(), chat_id_list[i].strip())

msg_sched.start()
warn_sched.start()