from re import search
from django.urls import path

from searchbar import views


urlpatterns = [
    
    path('', views.videodata) ,
    path('home/<str:videoid>',views.player, name='player'),
]   

