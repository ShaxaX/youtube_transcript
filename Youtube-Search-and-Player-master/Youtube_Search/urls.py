from django.contrib import admin
from django.urls import path , include
from django.conf.urls import handler404


urlpatterns = [
   path('admin/', admin.site.urls),
    path('', include('searchbar.urls'))
] 
    

handler404 = 'searchbar.views.error_404'
