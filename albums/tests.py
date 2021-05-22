import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Album
from albums.updateCurrentAlbum import current_album


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


class ScrapingTests(TestCase):

    def test_update_current_is_none_in_not_empty_db(self):
        """
        update_current should return None in a fresh testing database
        (I think that the album gets added when the database gets created)
        """
        self.assertIs(current_album(), None)

    def test_update_current_is_current_in_empty_db(self):
        """
        update_current should return the current album in a empty db
        """
        Album.objects.filter(id=1).delete()
        self.assertIs(Album.objects.count(), 0)
        todays_album = current_album()
        todays_album.save()
        self.assertIs(Album.objects.count(), 1)


class CurrentAlbumViewTests(TestCase):

    def test_no_current_album(self):
        """
        If no albums are in the database, an appropriate message is displayed
        """
        Album.objects.filter(id=1).delete()
        response = self.client.get(reverse('albums:current_album'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "There are no albums in the database")
        self.assertQuerysetEqual(response.context['current_album'], [])

    def test_current_album_exists(self):
        """
        If there is a current album, it is displayed on the page
        """
        response = self.client.get(reverse('albums:current_album'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "TODAYS ALBUM")


class IndexViewTests(TestCase):

    def test_no_albums(self):
        """
        If no albums exist, an appropriate message is displayed
        """
        Album.objects.filter(id=1).delete()
        response = self.client.get(reverse('albums:index'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "No albums are available")
        self.assertQuerysetEqual(response.context['latest_album_list'], [])

    def test_one_album(self):
        """
        If there is one album, it is displayed on the index page
        """
        Album.objects.filter(id=1).delete()
        album = create_album(title='1', artist_name='1', spotify_link='link', days=0)
        response = self.client.get(reverse('albums:index'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(response.context['latest_album_list'], [album])

    def test_six_albums(self):
        """
        If there are six albums, only the first 5 are displayed
        """
        Album.objects.filter(id=1).delete()
        album1 = create_album(title='1', artist_name='1', spotify_link='link', days=-5)
        album2 = create_album(title='2', artist_name='2', spotify_link='link', days=-4)
        album3 = create_album(title='3', artist_name='3', spotify_link='link', days=-3)
        album4 = create_album(title='4', artist_name='4', spotify_link='link', days=-2)
        album5 = create_album(title='5', artist_name='5', spotify_link='link', days=-1)
        album6 = create_album(title='6', artist_name='6', spotify_link='link', days=0)
        response = self.client.get(reverse('albums:index'))
        self.assertEquals(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['latest_album_list'],
            [album6, album5, album4, album3, album2]
        )


class AlbumInfoViewTests(TestCase):

    def test_album_info(self):
        """
        The info view of an album shows that albums information
        """
        Album.objects.filter(id=1).delete()
        album = create_album(title='1989', artist_name='Taylor Swift', spotify_link='link', days=0)
        response = self.client.get(album.get_absolute_url())
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, album.title)
