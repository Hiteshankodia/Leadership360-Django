from django.db import models


class Participant(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=100)
    department = models.IntegerField(max_length=100)
    location = models.CharField(max_length=100)
    email = models.EmailField()
    dob = models.DateField()
    country = models.IntegerField(max_length=100)
    state = models.IntegerField(max_length=100)