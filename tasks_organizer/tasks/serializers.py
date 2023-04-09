from rest_framework import serializers
from tasks.models import Task


class TasksSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    finished = serializers.BooleanField()
    parent_task = serializers.CharField(read_only=True)
