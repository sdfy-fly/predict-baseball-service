from django.urls import path 

from .views import index, auth, getCards


urlpatterns = [
    path('', index , name='home') ,
    path('get-cards', getCards , name='getCards') ,
    path('auth', auth , name='getCards') ,
    
]