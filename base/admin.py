from django.contrib import admin
from .models import Task, BaseAppInfo

admin.site.register(Task)
admin.site.register(BaseAppInfo)
