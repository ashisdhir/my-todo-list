from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.details, name='details'),
    path('author_details/', views.author_details, name='author_details'),
    path('accounts/login/', auth_views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    # path('todo_new/', views.todo_new, name='todo_new'),
    # path('todo_new/', views.todo_new_tmp1, name='todo_new'),
    # path('todo_new/', views.todo_new_tmp, name='todo_new'),
    # path('todo_new/', views.manage_books, name='todo_new'),
    path('todo_new/', views.todo_new_tmp2, name='todo_new'),
    path('edit/<int:title_id>/', views.todo_new_tmp2, name='edit'),
    # path('todo_new_add/', views.todo_new_add, name='todo_new_add'),
]