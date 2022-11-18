from apscheduler.schedulers.blocking import BlockingScheduler
from main import extract_data, send_details, send_warnings
from config import CONFIG
job_sched = BlockingScheduler()

def data_extracting_job():
    print(f'This jib runs every {CONFIG.TIME_INTERVAL} hours and extract data from the website')
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

# job_sched.add_job(data_extracting_job, 'interval', seconds=10) #For testing purpose
#Extracts data every 3 hours
job_sched.add_job(data_extracting_job, 'interval', hours=CONFIG.TIME_INTERVAL)
#Send attendance at 9 AM IST and 9 PM IST
job_sched.add_job(msg_sending_job, 'cron', hour = '3', minute = '30')
job_sched.add_job(msg_sending_job, 'cron', hour = '15', minute = '30')
#Send warning at 9:30 AM IST and 9:30 PM IST
job_sched.add_job(warn_sending_job, 'cron', hour='4', minute='00')
job_sched.add_job(warn_sending_job, 'cron', hour='16', minute='00')

print("Starting the scheduler")
job_sched.start()