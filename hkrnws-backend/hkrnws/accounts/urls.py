from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from .views import user_registration


urlpatterns = [
    url(
        r"api/users/register/", user_registration, name="user_registration",
    ),
    url(
        r'api-token-auth/', obtain_auth_token, name='api_token_auth'
    ),
]