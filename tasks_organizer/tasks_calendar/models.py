from django.db import models
from tasks.models import Task


class TaskDate(models.Model):
    """
    Class representing the tasks time aspect

    Fields:
        start_time (): Information about when task will be started.
        finish_time (): Information about when task need be finished.
        task (ForeignKey): Associated task pk.
    """
    start_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
