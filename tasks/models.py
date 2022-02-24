from django.db import models
from django.db.models import signals
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.timezone import now

STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("IN_PROGRESS", "IN_PROGRESS"),
    ("COMPLETED", "COMPLETED"),
    ("CANCELLED", "CANCELLED"),
)


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    priority = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class History(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    old_status = models.CharField(max_length=100)
    new_status = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    send_time = models.TimeField()
    last_report = models.DateTimeField(null=True, default=now)

    def __str__(self):
        return self.send_time


def update_history(instance, **kwargs):
    try:
        task = Task.objects.get(id=instance.id)
    except:
        task = None
    if task is not None and instance.status != task.status:
        History.objects.create(
            task=task, old_status=task.status, new_status=instance.status
        )


def report(instance, **kwargs):
    user = None
    report = None
    try:
        user = User.objects.get(pk=instance.id)
        report = Report.objects.get(user=user)
    except:
        pass

    if user is not None and report is None:
        time = datetime.strptime("0:0:0", "%H:%M:%S").time()
        Report.objects.create(user=user, send_time=time)


signals.pre_save.connect(receiver=update_history, sender=Task)
signals.pre_save.connect(receiver=report, sender=User)
