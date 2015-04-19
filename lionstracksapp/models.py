from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HealthMetric(models.Model):
    # user needs to be set to the logged in user's email address
    user = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=500)
    amount = models.IntegerField(default=0)
    unit = models.CharField(max_length=100)
    date = models.DateTimeField()

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email_address = models.CharField(max_length=200)
    #user_id = models.IntegerField(unique=True)

class UserToMetricMap(models.Model):
    email = models.CharField(max_length=200)
    user = models.CharField(max_length=200)