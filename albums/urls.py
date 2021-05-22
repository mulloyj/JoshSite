from django.urls import path

from . import views

app_name = 'albums'
urlpatterns = [
    path('', views.AlbumIndexView.as_view(), name='index'),
    # I dont think the following 2 urls are formatted correctly, but this works as is
    # If a album every got added that was simply named 'today' this would be a problem
    path('today/', views.CurrentAlbumView.as_view(), name='current_album'),
    path('<slug:slug>/', views.AlbumInfoView.as_view(), name='album_info'),
]
