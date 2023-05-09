import schedule
import routines as r

schedule.every(10).minutes.do(r.update_all_user_tasks())
schedule.every(1).day.do(r.update_tasks())
