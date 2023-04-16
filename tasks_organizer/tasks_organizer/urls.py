"""
URL configuration for tasks_organizer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks.views import TasksList, CreateTask, EditTask, DeleteTask

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', TasksList.as_view(), name='tasks'),
    path('create_task/', CreateTask.as_view(), name='create_task'),
    path('edit_task/<int:pk>/', EditTask.as_view(), name='edit_task'),
    path('delete_task/<int:pk>/', DeleteTask.as_view(), name='delete_task')

]
