from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Poll(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    question = models.CharField(max_length=255)
    option1 = models.CharField(max_length=100)
    option2 = models.CharField(max_length=100)
    option3 = models.CharField(max_length=100)
    option4 = models.CharField(max_length=100)
    vote1 = models.IntegerField(default=0)
    vote2 = models.IntegerField(default=0)
    vote3 = models.IntegerField(default=0)
    vote4 = models.IntegerField(default=0)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
