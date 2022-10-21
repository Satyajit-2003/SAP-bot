from apscheduler.schedulers.blocking import BlockingScheduler
from main import extract_data, send_details, send_warnings
from config import CONFIG
job_sched = BlockingScheduler()

def msg_sending_job():
    print(f'This job is runs every {CONFIG.TIME_INTERVAL} hours and send attendance by Telegram Bot')
    user_list = CONFIG.USERNAME.split(',')
    pass_list = CONFIG.PASSWORD.split(',')
    chat_id_list = CONFIG.TELEGRAM_CHAT_ID.split(',')
    for i in range(len(user_list)):
        extract_data(user_list[i].strip(), pass_list[i].strip())
        send_details(user_list[i].strip(), chat_id_list[i].strip())

def warn_sending_job():
    print("This job sends warning message to the user everyday at 4:30 PM GMT i.e. 10:00 PM IST")
    user_list = CONFIG.USERNAME.split(',')
    chat_id_list = CONFIG.TELEGRAM_CHAT_ID.split(',')
    for i in range(len(user_list)):
        send_warnings(user_list[i].strip(), chat_id_list[i].strip())

job_sched.add_job(msg_sending_job, 'interval', seconds = 180)
job_sched.add_job(warn_sending_job, 'cron', hour='16', minute='30')

print("Starting the scheduler")
job_sched.start()