from django.db import models
# Create your models here.
class HealthMetric(models.Model):
    user = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=500)
    amount = models.IntegerField(default=0)
    unit = models.CharField(max_length=100)
    date = models.DateTimeField()

