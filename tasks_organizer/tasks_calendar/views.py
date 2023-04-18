from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TaskDate
from tasks.models import Task


class TasksYear(APIView):
    """
    Show tasks list of one year ahead.
    """
    pass


class TasksQuarter(APIView):
    """
    Show tasks list of one quarter
    """
    pass


class TasksMonth(APIView):
    """
    Show tasks list of one month.
    """
    pass


class TasksWeek(APIView):
    """
    Show tasks list of one week.
    """
    pass


class TasksDay(APIView):
    """
    Show tasks list of one day.
    """
    pass


class AddTaskDate(APIView):
    """
    Add date and time to specific task.
    """
    pass


class EditTaskDate(APIView):
    """
    Edit date and time specific task.
    """
    pass


class DeleteTaskDate(APIView):
    """
    Delete date and time specific task.
    """
    pass
