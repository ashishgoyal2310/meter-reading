from django.contrib import admin
from meters.models import UserMeter, MeterHealth

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

