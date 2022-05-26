from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

admin.site.unregister(Site)
admin.site.unregister(Group)