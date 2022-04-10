from atexit import register
from django.urls import path,include
from . import views
from .views import CreateTask, Taskdetail, Tasklist, Taskupdate, Taskdelete, customLogin, registeruser
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('',Tasklist.as_view(), name='tasklist'),
    path('register/',registeruser.as_view(), name='register'),
    path('login/',customLogin.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('task/<int:pk>/',Taskdetail.as_view(), name='task'),
    path('createtask',CreateTask.as_view(), name='createtask'),
    path('updatetask/<int:pk>/',Taskupdate.as_view(), name='updatetask'),
    path('deletetask/<int:pk>/',Taskdelete.as_view(), name='deletetask'),
]
