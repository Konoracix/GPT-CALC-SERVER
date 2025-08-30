from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

class DeviceOnlyViewSet(ViewSet):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "Authorization",
                openapi.IN_HEADER,
                description="UUID urządzenia, np. 'Device <uuid>'",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_STRING),
                "mail": openapi.Schema(type=openapi.TYPE_STRING)
            }
        )}
    )
    def list(self, request):
        device = request.user
        return Response({"id": str(device.id), "mail": device.mail})
