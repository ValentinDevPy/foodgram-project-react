from django.contrib import admin

from users.models import Subscribe, User


class UserAdmin(admin.ModelAdmin):
    list_filter = ("email", "username")


admin.site.register(Subscribe)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
