from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task
from .serializers import TasksSerializer


# Create your tests here.
class TasksAPITest(APITestCase):
    def setUp(self):
        self.url = reverse('tasks')
        self.task1 = Task.objects.create(name='test1')
        self.task2 = Task.objects.create(name='test2')

    def test_get_all_tasks(self):
        response = self.client.get(self.url, format='json')
        models = Task.objects.all()
        serializer = TasksSerializer(models, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.data[0], dict(serializer.data[0]))


class CreateTaskViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('create_task')
        self.valid_payload = {'name': 'Test name', 'finished': True}
        self.invalid_payload = {'name': ''}

    def test_valid_post_request(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)

    def test_invalid_post_request(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Task.objects.count(), 0)


class EditTaskViewTestCase(APITestCase):
    def setUp(self):
        self.my_task = Task.objects.create(name='next_task')
        self.url = reverse('edit_task', args=[self.my_task.pk])
        self.valid_payload = {'name': 'Updated name', 'finished': True}
        self.invalid_payload = {'name': ''}

    def test_valid_put_request(self):
        response = self.client.put(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.get(pk=self.my_task.pk).name, 'Updated name')

    def test_invalid_put_request(self):
        response = self.client.put(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteTaskViewTest(APITestCase):

    def setUp(self):
        self.my_task = Task.objects.create(name='test task')
        self.url = reverse('delete_task', args=[self.my_task.pk])

    def test_delete_task(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=self.my_task.pk).exists())
