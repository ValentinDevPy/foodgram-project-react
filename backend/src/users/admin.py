from django.contrib import admin

from users.models import Subscribe, User
from django.contrib.auth.admin import UserAdmin


class UserAdminCustom(UserAdmin):
    list_filter = ("email", "username")


admin.site.register(Subscribe)
admin.site.unregister(User)
admin.site.register(User,UserAdminCustom)
