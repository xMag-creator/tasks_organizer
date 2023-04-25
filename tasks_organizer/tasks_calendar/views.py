from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import TaskDate
from .serializers import CalendarSerializer
from datetime import datetime
from django.utils.dateparse import parse_datetime


class AllTasksDates(APIView):
    """
    Show list of tasks dates.
    """
    def get(self, request):
        tasks_dates_query = TaskDate.objects.all().order_by('start_time')
        serializer = CalendarSerializer(tasks_dates_query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddTaskDate(APIView):
    """
    Add date and time to specific task.
    """
    def post(self, request):
        serializer = CalendarSerializer(data=request.data)
        all_tasks_dates = TaskDate.objects.all()

        if serializer.is_valid():
            request_start_time = parse_datetime(request.data.get('start_time'))
            request_finish_time = parse_datetime(request.data.get('finish_time'))

            if request_start_time >= request_finish_time:
                """
                start_time != finish_time
                """
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if TaskDate.objects.filter(start_time=request.data.get('start_time')).exists():
                """
                start_time must be unique
                """
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if TaskDate.objects.filter(finish_time=request.data.get('finish_time')).exists():
                """
                finish_time must be unique
                """
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            for task_date in all_tasks_dates:
                if task_date.start_time < request_start_time < task_date.finish_time:
                    """
                    start_time can't be inside other record
                    """
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                if task_date.start_time < request_finish_time < task_date.finish_time:
                    """
                    finish_time can't be inside other record
                    """
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                if request_start_time < task_date.start_time < task_date.finish_time < request_finish_time:
                    """
                    new record can't overtake other record
                    """
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                if request_start_time.date() != request_finish_time.date():
                    """
                    new start_time and finish_time must have the same date
                    """
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                # new start_time and finish_time can't null
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
