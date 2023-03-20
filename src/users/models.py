from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, login, password, **extra_fields):
        if not email:
            raise ValueError(
                _('You must provide an email address')
            )

        if not login:
            raise ValueError(
                _('You must provide login')
            )

        email = self.normalize_email(email)
        user = self.model(email=email, login=login, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, login, password, **extra_fields):
        """
        Create and save a User with the given email, login and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                _("Superuser must be assigned to is_staff = True")
            )

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                _("Superuser must be assigned to is_superuser = True")
            )

        return self.create_user(email, login, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    login = models.CharField(max_length=50, unique=True)
    # User status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login',]

    def __str__(self):
        return self.login
