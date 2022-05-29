import factory
import factory.fuzzy
from app.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = "test name"
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password")

    class Meta:
        model = User
        django_get_or_create = ("email",)
