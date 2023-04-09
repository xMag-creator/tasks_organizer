from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TasksSerializer


class TasksList(APIView):
    """
    Get all tasks.
    """
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTask(APIView):
    """
    Create new task.
    """
    def post(self, request):
        serializer = TasksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditTask(APIView):
    def put(self, request):
        pass


class DeleteTask(APIView):
    def delete(self, request):
        pass
