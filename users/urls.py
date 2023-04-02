from django.urls import path

from .views import Auth, UserCards,  GetUserInfo, GetUpdatedUserData

urlpatterns = [
    path('api/get-cards', UserCards.as_view(), name='getCards'),
    path('api/auth', Auth.as_view(), name='auth'),
    path('api/user-info', GetUserInfo.as_view(), name='userInfo'),
    path('api/office', GetUpdatedUserData.as_view(), name='update-user-data')
]
