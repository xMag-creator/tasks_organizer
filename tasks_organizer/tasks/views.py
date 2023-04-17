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
        tasks_trees = Task.objects.filter(parent_task=None)
        result = self.get_tasks_tree(tasks_trees)
        return Response(result)

    def get_tasks_tree(self, tasks_trees):
        result = []
        for tasks_tree in tasks_trees:
            data = {
                'id': tasks_tree.id,
                'name': tasks_tree.name,
                'finished': tasks_tree.finished,
                'parent_task': tasks_tree.parent_task,

            }
            children = tasks_tree.children.all()
            if children:
                data['children'] = self.get_tasks_tree(children)
            result.append(data)
        return result


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
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        my_task = self.get_object(pk)
        serializer = TasksSerializer(my_task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteTask(APIView):
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
