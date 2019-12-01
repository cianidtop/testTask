from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
import json
from django.db.models.signals import post_save,pre_save
import requests
from .asana_api import create_project,update_project_name,create_task,update_task,change_task_project

class AsanaUser(models.Model):
	asana_id = models.CharField(max_length=50)
	name = models.CharField(max_length=30)

class Project(models.Model):
	name = models.CharField(max_length=30)
	asana_id = models.CharField(max_length=50,null=True, blank=True)

	def __str__(self):
		return self.name


class Task(models.Model):
	text = models.TextField(max_length=500)
	responsible = models.ForeignKey(
		AsanaUser,
		on_delete=models.CASCADE,
		related_name='tasks'
	)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	asana_id = models.CharField(max_length=50,null=True, blank=True)

@receiver(post_save, sender=Project)
def project_handler(sender,instance,created, **kwargs):
	if created:
		asana_id=create_project(instance.name)
		if (asana_id):
			instance.asana_id = asana_id
			post_save.disconnect(project_handler,sender=sender)
			instance.save()
			post_save.connect(project_handler,sender=sender)

	else:
		update_project_name(instance.asana_id,instance.name)

@receiver(post_save, sender=Task)
def task_handler(sender,instance,created, **kwargs):
	if created:
		asana_id=create_task(instance.text,instance.responsible.asana_id,instance.project.asana_id)
		if (asana_id):
			instance.asana_id = asana_id
			post_save.disconnect(task_handler,sender=sender)
			instance.save()
			post_save.connect(task_handler,sender=sender)
	else:
		update_task(instance.asana_id,instance.text,instance.responsible.asana_id,instance.project.asana_id)

@receiver(pre_save, sender=Task)
def task_handler_pre_save(sender,instance, **kwargs):
	print(instance.id)
	if instance.id:
		old_instance = Task.objects.get(pk=instance.id)
		if old_instance.project.asana_id!=instance.project.asana_id:
			change_task_project(instance.asana_id,old_instance.project.asana_id,instance.project.asana_id)