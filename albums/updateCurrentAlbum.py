from albums.models import Album
from django.utils import timezone

from bs4 import BeautifulSoup

import datetime
import requests
import re


def update_current_album():
    url = 'https://1001albumsgenerator.com/mulloy'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    title = get_album_title(soup)
    if title != Album.objects.order_by('date_listened_to')[0]:
        artist = get_artist_name(soup)
        link = get_spotify_link(soup)
        now = timezone.now().date()

        current_album = Album(title=title, artist_name=artist, spotify_link=link, date_listened_to=now)
        current_album.save()


def get_album_title(soup):
    result = soup.find(id='current-album-wrapper')
    return result.find('h1', class_='h2').text


def get_artist_name(soup):
    result = soup.find(id='current-album-wrapper')
    return result.findAll('h2', class_='h5')[0].text.split('\n')[0]


def get_spotify_link(soup):
    return soup.findAll('a', attrs={'href': re.compile("spotify")})[0].get('href')
