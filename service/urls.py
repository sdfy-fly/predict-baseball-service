from django.urls import path 

from .views import index,Auth, UserCards, PlayersDetail , GetSchesule, GetInjuryNews, GetUserInfo, CreatePaymentUrl


urlpatterns = [
    path('', index , name='home') ,
    path('api/get-cards', UserCards.as_view() , name='getCards') ,
    path('api/auth', Auth.as_view() , name='auth') ,  
    path('api/players-detail', PlayersDetail.as_view() , name='playersDetail') ,  
    path('api/schedule', GetSchesule.as_view() , name='schedule') ,  
    path('api/injury', GetInjuryNews.as_view() , name='injury') ,  
    path('api/user-info', GetUserInfo.as_view() , name='userInfo') ,  
    path('api/invoice/create', CreatePaymentUrl.as_view() , name='create-payment') ,  
]