import factory
import factory.fuzzy
from app.posts.models import Post


class PostFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory("app.users.tests.factories.UserFactory")
    body = factory.fuzzy.FuzzyText(length=100)
    like = []
    unlike = []

    class Meta:
        model = Post
