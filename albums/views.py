from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Album

import albums.updateCurrentAlbum as Update


# Create your views here.
class AlbumIndexView(generic.ListView):
    # Old, hard way to do this
    # latest_album_list = Album.objects.order_by('release_date')[:5]
    # template = loader.get_template('albums/index.html')
    # context = {
    #     'latest_album_list': latest_album_list,
    # }
    # return HttpResponse(template.render(context, request))
    template_name = 'albums/index.html'
    context_object_name = 'latest_album_list'

    def get_queryset(self):
        """Return the last 5 albums"""
        return Album.objects.order_by('date_listened_to')[:5]


class AlbumInfoView(generic.DetailView):
    # Old, hard way to do this
    # try:
    #     album = Album.objects.get(title=album_title)
    # except Album.DoesNotExist:
    #     raise Http404("Album does not exist")
    # return render(request, 'albums/album_info.html', {'album': album})
    model = Album
    template_name = 'albums/album_info.html'


class CurrentAlbumView(generic.ListView):
    Update.update_current_album()
    context_object_name = 'current_album'
    template_name = 'albums/current_album.html'

    def get_queryset(self):
        return Album.objects.order_by('date_listened_to')[0]
