from django.db import models

# Create your models here.
class Summary(models.Model):
    temp = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    Red = models.BooleanField()
    Green = models.BooleanField()
    Blue = models.BooleanField()
    distance = models.FloatField()
    

