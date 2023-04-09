from django.db import models


class Task(models.Model):
    """
    Class representing the structure of task to be performed.

    Fields:
        name (CharField): Task name.
        finished (BooleanField): Information about completing the task.
        parent_task (ForeignKey): Parent task pk.
    """
    name = models.CharField(max_length=256)
    finished = models.BooleanField(default=False)
    parent_task = models.ForeignKey('self',
                                    on_delete=models.CASCADE,
                                    null=True,
                                    blank=True,
                                    related_name='children')
