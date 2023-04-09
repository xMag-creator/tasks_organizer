from rest_framework import serializers
from tasks.models import Task


class TasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'finished', 'parent_task')
