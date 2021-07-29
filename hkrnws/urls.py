from django.contrib import admin
from django.urls import path

from .accounts.urls import urlpatterns as account_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += account_urlpatterns