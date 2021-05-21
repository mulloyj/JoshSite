from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.template import loader

from .models import Album


# Create your views here.
def index(request):
    # This is the hard way to do this
    # latest_album_list = Album.objects.order_by('release_date')[:5]
    # template = loader.get_template('albums/index.html')
    # context = {
    #     'latest_album_list': latest_album_list,
    # }
    # return HttpResponse(template.render(context, request))
    latest_album_list = Album.objects.order_by('release_date')[:5]
    context = {'latest_album_list': latest_album_list}
    return render(request, 'albums/index.html', context)


def album_info(request, album_title):
    # this is the hard way to do this
    # try:
    #     album = Album.objects.get(title=album_title)
    # except Album.DoesNotExist:
    #     raise Http404("Album does not exist")
    # return render(request, 'albums/album_info.html', {'album': album})
    album = get_object_or_404(Album, title=album_title)
    return render(request, 'albums/album_info.html', {'album': album})
