from django.db import models
from django.apps import AppConfig
from django.contrib.auth.models import User




class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['complete']


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class BaseAppInfo(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description


class BaseConfig(AppConfig):
    name = 'base'

    def ready(self):
        import base.signals


class EmailLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user_email = models.EmailField()
    subject = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.timestamp} - {self.user_email} - {self.subject}"
