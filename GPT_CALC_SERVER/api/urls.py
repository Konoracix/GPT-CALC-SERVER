from django.urls import path
from .views import sendRequest, getAllDevices

urlpatterns = [
    path('chat/<str:id>', sendRequest, name='chat'),
		path('devices', getAllDevices),
]