from django.urls import path
from api.views import GPTManagerViewSet, DeviceViewSet, DeviceOnlyViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register("chat", GPTManagerViewSet, basename="chat")
router.register("device", DeviceViewSet, basename="device")
router.register("auth", DeviceOnlyViewSet, basename="auth")

urlpatterns = router.urls