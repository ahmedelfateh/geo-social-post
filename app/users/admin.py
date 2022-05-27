from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from app.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "first_name")
    readonly_fields = ("email", "first_name", "geo_data", "register_in_holiday")
    fields = ("email", "first_name", "geo_data", "register_in_holiday")
    search_fields = ("email", "first_name")


admin.site.unregister(Site)
admin.site.unregister(Group)
