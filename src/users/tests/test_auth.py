import pytest
from django.conf import settings
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_register():

    body = {
        "email": "goreva@gmail.com",
        "username": "goreva",
        "password1": "password1234321",
        "password2": "password1234321"
    }

    response = APIClient().post(
        path='/api/register/',
        data=body,
        format="json",
    )

    assert response.status_code == 201  # type: ignore


@pytest.mark.django_db
def test_login_logout(test_user):

    expected_status_code = 200

    body = {
        "email": "user@user.com",
        "password": "foobar",
    }

    # login user
    response = APIClient().post(
        path='/api/login/',
        data=body,
        format="json",
    )

    assert response.status_code == expected_status_code, (  # type: ignore
        "Make sure that existing user can log in with his login and password"
    )

    assert settings.REST_AUTH["JWT_AUTH_COOKIE"] in response.cookies  # type: ignore
    assert settings.REST_AUTH["JWT_AUTH_REFRESH_COOKIE"] in response.cookies  # type: ignore

    # logout user
    response = APIClient().post(
        path='/api/logout/',
    )

    assert response.status_code == expected_status_code, (  # type: ignore
        "Make sure that logged in user can log out"
    )
