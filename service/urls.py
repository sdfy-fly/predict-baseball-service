from django.urls import path 

from .views import index, auth, getCards,Auth , Action


urlpatterns = [
    path('', index , name='home') ,
    path('get-cards', getCards , name='getCards') ,
    # path('auth', auth , name='getCards') ,
    path('auth', Auth.as_view() , name='getCards') ,
    path('action', Action.as_view() , name='dfgrefgh') ,
    
]