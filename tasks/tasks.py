import datetime
from datetime import datetime, timedelta, timezone

from celery.decorators import periodic_task
from celery.schedules import crontab
from django.contrib.auth.models import User
from django.core.mail import send_mail
from task_manager.celery import app

from tasks.models import *


def send_user(user):
    tasks = Task.objects.filter(user=user)
    pending = tasks.filter(status="PENDING").count()
    in_progress = tasks.filter(status="IN_PROGRESS").count()
    completed = tasks.filter(status="COMPLETED").count()
    cancelled = tasks.filter(status="CANCELLED").count()

    message = f"""Hi {user.username},
    Here is your status for your task list
    Number of pending tasks: {pending}
    Tasks in progress {in_progress}
    Completed tasks : {completed}
    Cancelled tasks : {cancelled}
    Total tasks created : {tasks}
    """
    send_mail("Task List", message, "manager@company.com", [user.email])


@periodic_task(run_every=timedelta(minutes=15))
def send_sheduled_mails():
    times = Report.objects.filter(
        send_time__lte=datetime.now(timezone.utc),
        last_report__lte=datetime.now(timezone.utc).date() - timedelta(minutes=15),
    ).order_by("user_id")
    print("wave")
    for i in times:
        try:
            send_user(i.user)
            i.last_report = datetime.now(timezone.utc)
            i.save()
        except:
            pass
