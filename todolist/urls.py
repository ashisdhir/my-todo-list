from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('details/', views.details, name='details'),
    path('todo_new/', views.todo_new, name='todo_new'),
]