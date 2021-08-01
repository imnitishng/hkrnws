from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token

from .views import posts_list, post


urlpatterns = [
    url(
        r"api/posts/", posts_list, name="posts_list",
    ),
    url(
        r"api/post/", post, name="post",
    ),
]
