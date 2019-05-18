from django.contrib import admin

from .models import TaskTree, TaskType, Task, Statements
# Register your models here.

admin.site.register(TaskTree)
admin.site.register(TaskType)
admin.site.register(Task)
admin.site.register(Statements)
