import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
@pytest.mark.django_db
def test_user():
    User = get_user_model()

    User.objects.create_user(
        email="user@user.com",
        login="userlogin",
        password="foobar",
    )