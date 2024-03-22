from django.contrib import admin

from admins.models import Admin


@admin.register(Admin)
class AdminsAdmin(admin.ModelAdmin):
    pass
