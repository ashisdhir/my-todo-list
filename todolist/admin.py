from django.contrib import admin
from .models import TodoTitle, TodoDetail, Author, Book

# Register your models here.
admin.site.register(TodoTitle)
admin.site.register(TodoDetail)
admin.site.register(Author)
admin.site.register(Book)
