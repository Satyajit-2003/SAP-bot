from apscheduler.schedulers.blocking import BlockingScheduler
from main import extract_data, send_details, send_warnings
from config import CONFIG
job_sched = BlockingScheduler()

def data_extracting_job():
    user_list = CONFIG.USERNAME.split(',')
    pass_list = CONFIG.PASSWORD.split(',')
    for i in range(len(user_list)):
        extract_data(user_list[i].strip(), pass_list[i].strip())

def msg_sending_job():
    print(f'This job sends attendance details to the user everyday at 4:30 PM GMT i.e. 10:00 PM IST and 15:30 PM GMT i.e. 21:00 PM IST')
    user_list = CONFIG.USERNAME.split(',')
    chat_id_list = CONFIG.TELEGRAM_CHAT_ID.split(',')
    for i in range(len(user_list)):
        send_details(user_list[i].strip(), chat_id_list[i].strip())

def warn_sending_job():
    print("This job sends warning message to the user everyday at 4:30 PM GMT i.e. 10:00 PM IST and 16:00 PM GMT i.e. 21:30 PM IST")
    user_list = CONFIG.USERNAME.split(',')
    chat_id_list = CONFIG.TELEGRAM_CHAT_ID.split(',')
    for i in range(len(user_list)):
        send_warnings(user_list[i].strip(), chat_id_list[i].strip())

#Extracts data 
job_sched.add_job(data_extracting_job, 'interval', hours=int(CONFIG.UPDATE_INTERVAL))

#Send attendance 
for time in CONFIG.ATTENDANCE_TIME.split(','):
    hour, minute = time.strip().split(':')
    job_sched.add_job(msg_sending_job, 'cron', hour=hour, minute=minute)

#Send warning 
for time in CONFIG.WARNING_TIME.split(','):
    hour, minute = time.strip().split(':')
    job_sched.add_job(warn_sending_job, 'cron', hour=hour, minute=minute)

print("The scheduler has started")
job_sched.start()