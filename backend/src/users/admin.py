from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Subscribe, User


class UserAdminCustom(UserAdmin):
    list_filter = ("email", "username")


admin.site.register(Subscribe)
admin.site.unregister(User)
admin.site.register(User, UserAdminCustom)
