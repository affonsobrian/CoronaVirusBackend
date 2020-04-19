from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=255, blank=False, null=True)
    coordinate_x = models.FloatField(null=True);
    coordinate_y = models.FloatField(null=True);
    points = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

    def __repr__(self):
        return str(self.user)


class NotificationType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Notification(models.Model):
    message = models.CharField(max_length=255)
    notification_type = models.ForeignKey(NotificationType, on_delete=models.CASCADE, null=False)
    event_run = models.BooleanField(default=False)
    time_run = models.BooleanField(default=False)
    time = models.TimeField(default=datetime.now)

    def __str__(self):
        return self.message
    
    def __repr__(self):
        return self.message