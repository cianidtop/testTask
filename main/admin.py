from django.contrib import admin
from .models import Project,Task,AsanaUser

admin.site.register(Project)
admin.site.register(AsanaUser)
admin.site.register(Task)