from django_apscheduler.jobstores import DjangoJobStore, DjangoJob
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from .tasks import notify_subscribers

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Запланировать задачу на каждую неделю (например, каждый понедельник в 8:00)
    scheduler.add_job(
        notify_subscribers,
        trigger=CronTrigger(day_of_week='mon', hour=8, minute=0),
        id='weekly_newsletter',  # Идентификатор задачи
        replace_existing=True,
    )

    scheduler.start()
