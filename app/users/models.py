from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):
    # pylint: disable=arguments-differ
    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return super().create_user("", email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return super().create_superuser("", email, password, **extra_fields)


class User(AbstractUser):

    username = None  # type: ignore
    email = models.EmailField(_("Email"), blank=True, unique=True)
    geo_data = models.JSONField(_("GEO Data"), blank=True, null=True)
    register_in_holiday = ArrayField(
        models.CharField(max_length=30, blank=True), size=10, blank=True, null=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    class Meta:
        ordering = ["first_name", "email"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.first_name} ({self.email})"
