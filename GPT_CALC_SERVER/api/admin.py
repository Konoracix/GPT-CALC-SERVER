from django.contrib import admin
from api.models import Device

# Register your models here.
class DeviceAdmin(admin.ModelAdmin):
		readonly_fields = ['id', 'created_at', 'updated_at']

admin.site.register(Device, DeviceAdmin)