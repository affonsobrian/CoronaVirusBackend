from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(max_length=255, blank=False, null=True)
    coordinate_x = models.FloatField(null=True);
    coordinate_y = models.FloatField(null=True);
    points = models.IntegerField(default=0)
