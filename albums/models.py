from django.db import models
from django.utils import timezone

import datetime


# Create your models here.
class Album(models.Model):
    title = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    spotify_link = models.CharField(max_length=200)
    date_listened_to = models.DateField()

    def __str__(self):
        return self.title

    def was_listened_to_recently(self):
        now = timezone.now()
        return (now - datetime.timedelta(days=7)).date() <= self.date_listened_to <= now.date()
