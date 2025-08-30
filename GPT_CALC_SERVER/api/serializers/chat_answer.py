from rest_framework import serializers
from api.models import Device

class ChatAnswerSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    device = serializers.UUIDField(read_only=True)
    prompt = serializers.CharField(required=True, max_length=500)
    answer = serializers.CharField(required=True, max_length=500)