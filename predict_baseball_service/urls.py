from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('service.urls')),
    path('', include('payment.urls')),
    path('', include('users.urls')),
]
