from django.urls import path 

from .views import index, auth, getCards,Auth, UserCards


urlpatterns = [
    path('', index , name='home') ,
    path('api/get-cards', UserCards.as_view() , name='getCards') ,
    path('api/auth', Auth.as_view() , name='auth') ,  
]