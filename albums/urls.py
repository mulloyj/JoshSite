from django.urls import path

from . import views

app_name = 'albums'
urlpatterns = [
    path('', views.AlbumIndexView.as_view(), name='index'),
    path('<slug:slug>/', views.AlbumInfoView.as_view(), name='album_info'),
]
