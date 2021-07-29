from django.conf.urls import url

from .views import user_registration


urlpatterns = [
    url(
        r"users/register/", user_registration, name="user_registration"
    ),
]