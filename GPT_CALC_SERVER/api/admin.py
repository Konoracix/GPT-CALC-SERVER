from django.contrib import admin
from api.models import Device
from api.models import ChatAnswer

# Register your models here.
class DeviceAdmin(admin.ModelAdmin):
		readonly_fields = ['id', 'created_at', 'updated_at']


class ChatAnswerAdmin(admin.ModelAdmin):
		readonly_fields = ['id', 'created_at', 'updated_at']

admin.site.register(Device, DeviceAdmin)
admin.site.register(ChatAnswer, ChatAnswerAdmin)