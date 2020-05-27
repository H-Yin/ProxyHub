import time
from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler

def tick():
    print('Tick! The time is: %s' % datetime.now())
    time.sleep(20)

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'interval', seconds=3)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C    '))

    try:
        help(scheduler)
        scheduler.start()
        print("test")
    except (KeyboardInterrupt, SystemExit):
        pass
