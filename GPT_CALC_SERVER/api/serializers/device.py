from rest_framework import serializers
from api.models import Device

class DeviceSerializer(serializers.Serializer):
	id = serializers.UUIDField(read_only=True)
	mail = serializers.EmailField(max_length=254)
	number_of_requests = serializers.IntegerField(default=0)
	created_at = serializers.DateTimeField(read_only=True)
	updated_at = serializers.DateTimeField(read_only=True)
	deleted_at = serializers.DateTimeField(allow_null=True, required=False)

	def create(self, validated_data):
		return Device.objects.create(**validated_data)