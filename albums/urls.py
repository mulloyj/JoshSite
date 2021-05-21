from django.urls import path

from . import views

app_name = 'albums'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:album_title>/', views.album_info, name='album_info'),
]