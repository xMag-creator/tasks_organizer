from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from .models import TaskDate, Task
from .serializers import CalendarSerializer
from datetime import timedelta


class AllTasksDatesTestCase(APITestCase):
    """
    testing tasks dates view, method: GET
    """
    def setUp(self):
        self.url = reverse('all_tasks_dates')
        # times
        self.time_now = timezone.make_aware(timezone.datetime(2020, 1, 1, 12, 0, 0), timezone.get_current_timezone())
        self.time_first_hour = self.time_now + timedelta(hours=1)
        self.time_second_hour = self.time_now + timedelta(hours=2)
        self.time_third_hour = self.time_now + timedelta(hours=3)

        # tasks
        self.task1 = Task.objects.create(name='test1')
        self.task2 = Task.objects.create(name='test2')

        # tasksDates
        self.taskDate1_1 = TaskDate.objects.create(start_time=self.time_now,
                                                   finish_time=self.time_first_hour,
                                                   task=self.task1)
        self.taskDate1_2 = TaskDate.objects.create(start_time=self.time_second_hour,
                                                   finish_time=self.time_third_hour,
                                                   task=self.task1)
        self.taskDate2_1 = TaskDate.objects.create(start_time=self.time_first_hour,
                                                   finish_time=self.time_second_hour,
                                                   task=self.task1)

    def test_get_all_tasksDates(self):
        response = self.client.get(self.url, format='json')
        models = TaskDate.objects.all()
        serializer = CalendarSerializer(models, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.data[0], dict(serializer.data[0]))


class AddTaskDateTestCase(APITestCase):
    """
    testing add new task_date view, method: POST
    """
    def setUp(self):
        self.url = reverse('add_task_date')

        # times
        self.time_now = timezone.make_aware(timezone.datetime(2020, 1, 1, 12, 0, 0), timezone.get_current_timezone())
        self.time_minus_one_hour = self.time_now - timedelta(hours=1)
        self.time_first_hour = self.time_now + timedelta(hours=1)
        self.time_second_hour = self.time_now + timedelta(hours=2)
        self.time_third_hour = self.time_now + timedelta(hours=3)
        self.time_fourth_hour = self.time_now + timedelta(hours=4)
        self.time_fifth_hour = self.time_now + timedelta(hours=5)
        self.time_sixth_hour = self.time_now + timedelta(hours=6)
        self.time_seventh_hour = self.time_now + timedelta(hours=7)
        self.time_eighth_hour = self.time_now + timedelta(hours=8)
        self.time_ninth_hour = self.time_now + timedelta(hours=9)

        # tasks
        self.task1 = Task.objects.create(name='test1')
        self.task2 = Task.objects.create(name='test2')

        self.valid_payload = {'start_time': self.time_third_hour,
                              'finish_time': self.time_fourth_hour,
                              'task': self.task2.pk,
                              }
        self.invalid_type_payload = {'start_time': 3, 'finish_time': '12.12.12', 'task': self.task2.pk}
        self.invalid_order_payload = {'start_time': self.time_fourth_hour,
                                      'finish_time': self.time_third_hour,
                                      'task': self.task2.pk,
                                      }
        self.invalid_equal_payload = {'start_time': self.time_fourth_hour,
                                      'finish_time': self.time_fourth_hour,
                                      'task': self.task2.pk,
                                      }
        self.invalid_not_unique_start_payload = {'start_time': self.time_second_hour,
                                                 'finish_time': self.time_fourth_hour,
                                                 'task': self.task2.pk,
                                                 }
        self.invalid_not_unique_finish_payload = {'start_time': self.time_minus_one_hour,
                                                  'finish_time': self.time_first_hour,
                                                  'task': self.task2.pk,
                                                  }
        self.invalid_start_inside_other_payload = {'start_time': self.time_seventh_hour,
                                                   'finish_time': self.time_ninth_hour,
                                                   'task': self.task2.pk,
                                                   }
        self.invalid_finish_inside_other_payload = {'start_time': self.time_fifth_hour,
                                                    'finish_time': self.time_seventh_hour,
                                                    'task': self.task2.pk,
                                                    }
        self.invalid_overtake_payload = {'start_time': self.time_fifth_hour,
                                         'finish_time': self.time_ninth_hour,
                                         'task': self.task2.pk,
                                         }
        self.different_dates = {'start_time': self.time_third_hour,
                                'finish_time': self.time_fourth_hour + timedelta(days=1),
                                'task': self.task2.pk,
                                }
        self.null_data = {'start_time': '', 'finish_time': '', 'task': self.task2.pk}

        # tasksDates
        self.taskDate1_1 = TaskDate.objects.create(start_time=self.time_now,
                                                   finish_time=self.time_first_hour,
                                                   task=self.task1)
        self.taskDate1_2 = TaskDate.objects.create(start_time=self.time_second_hour,
                                                   finish_time=self.time_third_hour,
                                                   task=self.task1)
        self.taskDate2_1 = TaskDate.objects.create(start_time=self.time_first_hour,
                                                   finish_time=self.time_second_hour,
                                                   task=self.task2)
        self.taskDate2_2 = TaskDate.objects.create(start_time=self.time_sixth_hour,
                                                   finish_time=self.time_eighth_hour,
                                                   task=self.task2)

    def test_valid_post_request(self):
        """
        valid post request
        :return:
        """
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskDate.objects.count(), 5)

    def test_invalid_post_request(self):
        """
        wrong types of data
        :return:
        """
        response = self.client.post(self.url, self.invalid_type_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TaskDate.objects.count(), 4)

    def test_invalid_time_later(self):
        """
        start_time later that finish_time
        :return:
        """
        response = self.client.post(self.url, self.invalid_order_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TaskDate.objects.count(), 4)

    def test_invalid_time_same(self):
        """
        start_time the same as finish_time
        :return:
        """
        response = self.client.post(self.url, self.invalid_equal_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TaskDate.objects.count(), 4)

    def test_invalid_start_time_not_unique(self):
        """
        start_time must be unique
        :return:
        """
        response = self.client.post(self.url, self.invalid_not_unique_start_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TaskDate.objects.count(), 4)

    def test_invalid_finish_time_not_unique(self):
        """
        finish_time must be unique
        :return:
        """
        response = self.client.post(self.url, self.invalid_not_unique_finish_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TaskDate.objects.count(), 4)

    def test_invalid_start_time_inside(self):
        """
        start_time can't be inside other TaskDate record
        :return:
        """
        response = self.client.post(self.url, self.invalid_start_inside_other_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TaskDate.objects.count(), 4)

    def test_invalid_finish_time_inside(self):
        """
        finish_time can't be inside other TaskDate record
        :return:
        """
        response = self.client.post(self.url, self.invalid_finish_inside_other_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TaskDate.objects.count(), 4)

    def test_invalid_new_task_date_overtake_other(self):
        """
        new TaskDate overtake another TaskDate
        :return:
        """
        response = self.client.post(self.url, self.invalid_overtake_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TaskDate.objects.count(), 4)

    def test_task_date_have_different_dates(self):
        """
        new TaskDate need have the same start_time date and finish_time date
        :return:
        """
        response = self.client.post(self.url, self.different_dates, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TaskDate.objects.count(), 4)

    def test_null_task_data(self):
        """
        data can't be null
        :return:
        """
        response = self.client.post(self.url, self.null_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TaskDate.objects.count(), 4)


class EditTaskDateTestCase(APITestCase):
    """
    testing add new task_date view, method: PUT
    """
    def setUp(self):
        # times
        self.time_now = timezone.make_aware(timezone.datetime(2020, 1, 1, 12, 0, 0), timezone.get_current_timezone())
        self.time_minus_one_hour = self.time_now - timedelta(hours=1)
        self.time_first_hour = self.time_now + timedelta(hours=1)
        self.time_second_hour = self.time_now + timedelta(hours=2)
        self.time_third_hour = self.time_now + timedelta(hours=3)
        self.time_fourth_hour = self.time_now + timedelta(hours=4)
        self.time_fifth_hour = self.time_now + timedelta(hours=5)
        self.time_sixth_hour = self.time_now + timedelta(hours=6)
        self.time_seventh_hour = self.time_now + timedelta(hours=7)
        self.time_eighth_hour = self.time_now + timedelta(hours=8)
        self.time_ninth_hour = self.time_now + timedelta(hours=9)

        # tasks
        self.task1 = Task.objects.create(name='test1')
        self.task2 = Task.objects.create(name='test2')

        # tasksDates
        self.taskDate1_1 = TaskDate.objects.create(start_time=self.time_now,
                                                   finish_time=self.time_first_hour,
                                                   task=self.task1)
        self.taskDate1_2 = TaskDate.objects.create(start_time=self.time_second_hour,
                                                   finish_time=self.time_third_hour,
                                                   task=self.task1)
        self.taskDate2_1 = TaskDate.objects.create(start_time=self.time_first_hour,
                                                   finish_time=self.time_second_hour,
                                                   task=self.task2)
        self.taskDate2_2 = TaskDate.objects.create(start_time=self.time_sixth_hour,
                                                   finish_time=self.time_eighth_hour,
                                                   task=self.task2)

        self.valid_payload = {'start_time': self.time_third_hour,
                              'finish_time': self.time_fourth_hour,
                              'task': self.task1.pk,
                              }
        self.invalid_type_payload = {'start_time': 3, 'finish_time': '12.12.12', 'task': self.task2.pk}
        self.invalid_order_payload = {'start_time': self.time_fourth_hour,
                                      'finish_time': self.time_third_hour,
                                      'task': self.task2.pk,
                                      }
        self.invalid_equal_payload = {'start_time': self.time_fourth_hour,
                                      'finish_time': self.time_fourth_hour,
                                      'task': self.task2.pk,
                                      }
        self.invalid_not_unique_start_payload = {'start_time': self.time_second_hour,
                                                 'finish_time': self.time_fourth_hour,
                                                 'task': self.task2.pk,
                                                 }
        self.invalid_not_unique_finish_payload = {'start_time': self.time_minus_one_hour,
                                                  'finish_time': self.time_first_hour,
                                                  'task': self.task2.pk,
                                                  }
        self.invalid_start_inside_other_payload = {'start_time': self.time_seventh_hour,
                                                   'finish_time': self.time_ninth_hour,
                                                   'task': self.task2.pk,
                                                   }
        self.invalid_finish_inside_other_payload = {'start_time': self.time_fifth_hour,
                                                    'finish_time': self.time_seventh_hour,
                                                    'task': self.task2.pk,
                                                    }
        self.invalid_overtake_payload = {'start_time': self.time_fifth_hour,
                                         'finish_time': self.time_ninth_hour,
                                         'task': self.task2.pk,
                                         }
        self.different_dates = {'start_time': self.time_third_hour,
                                'finish_time': self.time_fourth_hour + timedelta(days=1),
                                'task': self.task2.pk,
                                }
        self.null_data = {'start_time': '', 'finish_time': '', 'task': self.task2.pk}

        # url
        self.url = reverse('edit_task_date', args=[self.taskDate1_1.pk])

    def test_valid_put_request(self):
        """
        valid put request
        :return:
        """
        response = self.client.put(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TaskDate.objects.get(pk=self.taskDate1_1.pk).start_time, self.time_third_hour)

    def test_invalid_put_request(self):
        """
        wrong types of data
        :return:
        """
        response = self.client.put(self.url, self.invalid_type_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(TaskDate.objects.count(), 4)

    def test_invalid_time_later(self):
        """
        start_time later that finish_time
        :return:
        """
        response = self.client.put(self.url, self.invalid_order_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_time_same(self):
        """
        start_time the same as finish_time
        :return:
        """
        response = self.client.put(self.url, self.invalid_equal_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_start_time_not_unique(self):
        """
        start_time must be unique
        :return:
        """
        response = self.client.put(self.url, self.invalid_not_unique_start_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_finish_time_not_unique(self):
        """
        finish_time must be unique
        :return:
        """
        response = self.client.put(self.url, self.invalid_not_unique_finish_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_start_time_inside(self):
        """
        start_time can't be inside other TaskDate record
        :return:
        """
        response = self.client.put(self.url, self.invalid_start_inside_other_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_finish_time_inside(self):
        """
        finish_time can't be inside other TaskDate record
        :return:
        """
        response = self.client.put(self.url, self.invalid_finish_inside_other_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_new_task_date_overtake_other(self):
        """
        new TaskDate overtake another TaskDate
        :return:
        """
        response = self.client.put(self.url, self.invalid_overtake_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_task_date_have_different_dates(self):
        """
        new TaskDate need have the same start_time date and finish_time date
        :return:
        """
        response = self.client.put(self.url, self.different_dates, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_null_task_data(self):
        """
        data can't be null
        :return:
        """
        response = self.client.put(self.url, self.null_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteTaskDataViewTestCase(APITestCase):
    """
        testing delete TaskDate view, method: DELETE
    """
    def setUp(self):
        self.time_now = timezone.make_aware(timezone.datetime(2020, 1, 1, 12, 0, 0), timezone.get_current_timezone())
        self.time_first_hour = self.time_now + timedelta(hours=1)
        self.task1 = Task.objects.create(name='test1')
        self.my_task_date = TaskDate.objects.create(start_time=self.time_now,
                                                    finish_time=self.time_first_hour,
                                                    task=self.task1,
                                                    )
        self.url = reverse('delete_task_date', args=[self.my_task_date.pk])

    def test_delete_task_date(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TaskDate.objects.filter(pk=self.my_task_date.pk).exists())

