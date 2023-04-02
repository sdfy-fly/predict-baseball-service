from django.urls import path

from .views import PlayersDetail, GetSchedule, GetInjuryNews

urlpatterns = [
    path('api/players-detail', PlayersDetail.as_view(), name='playersDetail'),
    path('api/schedule', GetSchedule.as_view(), name='schedule'),
    path('api/injury', GetInjuryNews.as_view(), name='injury'),
]
