from django.contrib import admin

# Register your models here.

from rest_framework_simplejwt import token_blacklist


class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):
    actions = ['delete_selected']

    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)
