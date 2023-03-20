import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.fixture
@pytest.mark.django_db
def authorized_client():

    user = get_user_model().objects.create_user(
        email="user@user.com",
        login="userlogin",
        password="foobar",
    )

    refresh_token = RefreshToken.for_user(user)

    authorized_client = APIClient()
    authorized_client.cookies[settings.REST_AUTH["JWT_AUTH_COOKIE"]] = refresh_token.access_token
    authorized_client.cookies[settings.REST_AUTH["JWT_AUTH_REFRESH_COOKIE"]] = refresh_token

    return authorized_client