from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
import os
from rest_framework import status
from api.models import Device, ChatAnswer
from api.serializers import DeviceSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from drf_yasg import openapi



class DeviceViewSet(GenericViewSet):
	permission_classes = [AllowAny] 
	serializer_class = DeviceSerializer
	queryset = Device.objects.all()
		
	@swagger_auto_schema()
	@action(detail=False, methods=["GET"])
	def get(self, request):
		device = Device.objects.all()
		serializer = self.get_serializer(device, many=True)
		return Response(serializer.data)

	@swagger_auto_schema()
	def create(self, request):
		serializer = self.get_serializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)