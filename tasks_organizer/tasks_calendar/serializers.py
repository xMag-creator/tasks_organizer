from rest_framework import serializers
from .models import TaskDate


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDate
        fields = ('id', 'task', 'start_time', 'finish_time')
