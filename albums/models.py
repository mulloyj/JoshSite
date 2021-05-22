from django.db import models
from django.utils import timezone
from django.urls import reverse

import datetime

# Create your models here.


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    spotify_link = models.CharField(max_length=200)
    date_listened_to = models.DateField()
    slug = models.SlugField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('albums:album_info', kwargs={'slug': self.slug})

    def was_listened_to_recently(self):
        now = timezone.now()
        return (now - datetime.timedelta(days=7)).date() <= self.date_listened_to <= now.date()

