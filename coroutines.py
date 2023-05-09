import schedule
import routines as r
import time

schedule.every(10).minutes.do(r.update_all_user_tasks)
schedule.every(1).day.do(r.update_tasks)

while True:
    schedule.run_pending()
    time.sleep(1)
