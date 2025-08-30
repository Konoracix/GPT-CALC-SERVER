from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from api.models import Device

class DeviceAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None 

        try:
            prefix, device_id = auth_header.split()
        except ValueError:
            raise AuthenticationFailed("Invalid Authorization header format. Use: Device <uuid>")

        if prefix.lower() != "device":
            return None

        try:
            device = Device.objects.get(id=device_id)
        except Device.DoesNotExist:
            raise AuthenticationFailed("Invalid device ID")

        return (device, None)
