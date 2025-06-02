from django.urls import path
from .views import sendRequest, getAllDevices, getOneDevice

urlpatterns = [
    path('chat/<str:id>', sendRequest, name='chat'),
		path('devices', getAllDevices),
		path('devices/<str:id>', getOneDevice),
]