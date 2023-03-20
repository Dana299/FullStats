import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_create_user():
    User = get_user_model()

    user = User.objects.create_user(
        email="user@user.com",
        login="userlogin",
        password="foobar",
    )

    assert user.email == "user@user.com"
    assert user.login == "userlogin"
    assert not user.is_staff
    assert not user.is_superuser

    with pytest.raises(ValueError):
        User.objects.create_user(
            email="",
            login="userlogin",
            password="foobar"
        )

    with pytest.raises(TypeError):
        User.objects.create_user(
            email="user@user.com",
            password="foobar"
        )

    with pytest.raises(ValueError):
        User.objects.create_user(
            email="user@user.com",
            login="",
            password="foobar",
        )
