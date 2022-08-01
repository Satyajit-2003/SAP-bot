from apscheduler.schedulers.blocking import BlockingScheduler
from main import extract_data, send_details

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=6)
def timed_job():
    print('This job is run every six hours.')
    extract_data()
    send_details()


sched.start()