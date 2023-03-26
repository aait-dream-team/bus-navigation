from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(hello_world, 'interval', minutes=1)
    scheduler.start()

def hello_world():
    print("hello world")
    open('readme other file.txt', 'w')