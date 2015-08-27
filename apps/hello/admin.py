from django.contrib import admin
from apps.hello.models import AppUser

# Register your models here.


class AppUserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False

admin.site.register(AppUser, AppUserAdmin)
