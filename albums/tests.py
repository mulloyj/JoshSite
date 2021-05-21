import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Album


def create_album(title='test', artist_name='test', spotify_link='test', days=0):
    """
    Create an album with the given 'title', 'artist_name', and 'spotify_link', 'days'
    is the offset from when the album was listened to, future is positive, past is negative
    """
    time = (timezone.now() + datetime.timedelta(days=days)).date()
    return Album.objects.create(title=title, artist_name=artist_name, spotify_link=spotify_link, date_listened_to=time)


# Create your tests here.
class AlbumModelTests(TestCase):

    def test_was_listened_to_recently_with_future_listening_time(self):
        """
        was_listened_to_recently returns False for albums listened to in the future.
        """
        future_album = create_album(days=1)
        self.assertIs(future_album.was_listened_to_recently(), False)

    def test_was_listened_to_recently_with_past_listening_time(self):
        """
        was_listened_to_recently returns False for albums listened to more than a week ago
        """
        past_album = create_album(days=-8)
        self.assertIs(past_album.was_listened_to_recently(), False)

    def test_was_listened_to_recently_with_recent_listening_time(self):
        """
        was_listened_to_recently returns True for albums listened to in the last week
        """
        recent_album = create_album(days=-7)
        self.assertIs(recent_album.was_listened_to_recently(), True)
