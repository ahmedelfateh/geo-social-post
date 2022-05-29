from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "app.posts"
    verbose_name = _("Posts")

    def ready(self):
        try:
            import app.users.signals  # noqa F401
        except ImportError:
            pass
