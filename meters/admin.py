from django.contrib import admin
from meters.models import UserMeter, MeterHealth, ApiGroup, ApiPermission

# Register your models here.

class UserMeterAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'user', 'meter_number']
    readonly_fields = ['install_date']
    raw_id_fields = ('user',)

admin.site.register(UserMeter, UserMeterAdmin)


class MeterHealthAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_meter_id', 'user_meter', 'reading_date']
    readonly_fields = ['reading_date']

admin.site.register(MeterHealth, MeterHealthAdmin)


class ApiPermissionAdmin(admin.ModelAdmin):
    pass
admin.site.register(ApiPermission, ApiPermissionAdmin)


class ApiGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('api_permissions', )
admin.site.register(ApiGroup, ApiGroupAdmin)
