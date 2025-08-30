from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from openai import OpenAI
from api.models import Device, ChatAnswer
from api.serializers import PromptSerializer, ChatAnswerSerializer
from api.permissions import IsDeviceAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import os


class GPTManagerViewSet(GenericViewSet):
	authentication_classes = []
	serializer_class = ChatAnswerSerializer
	queryset = ChatAnswer.objects.all()

	@swagger_auto_schema(
		request_body=PromptSerializer,
		manual_parameters=[
			openapi.Parameter(
				"Authorization",
				openapi.IN_HEADER,
				description="UUID urządzenia, np. 'Device <uuid>'",
				type=openapi.TYPE_STRING,
				required=True
			)
		]
	)
	@action(
		detail=True,
		methods=["POST"],
		serializer_class=PromptSerializer,
		permission_classes=[IsDeviceAuthenticated]
	)
	def answer(self, request, pk: int):
		serializer = PromptSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		OPENAI_KEY = os.environ.get("OPENAI_KEY")
		if not OPENAI_KEY:
			return Response(
				{"error": "OpenAI API key not configured"},
				status=status.HTTP_500_INTERNAL_SERVER_ERROR
			)

		client = OpenAI(
   			api_key=os.environ.get("OPENAI_KEY"),
    		http_client=httpx.Client(proxies=None)
		)

		try:
			device = Device.objects.get(id=pk)
			device.number_of_requests += 1
			device.save()
		except Device.DoesNotExist:
			raise NotFound(detail=f'Device with id: {pk} Not Found')

		prompt = serializer.validated_data["prompt"]

		basicPrompt = (
			"Jesteś asystentem pomagającym uczniom przy sciąganiu. "
			"Twoje odpowiedzi powinny być jak najbardziej zwięzłe i zawierać tylko kluczowe informacje. "
			"Maksymalnie kilka słów. Jeżeli pytasz o wzór, podaj tylko wzór. "
			"Nie formatuj tekstu. Ułamek dziesiętny podaj w ułamku zwykłym. "
			"Pytanie ucznia: "
		)

		response = client.chat.completions.create(
			model="o3-mini-2025-01-31",
			messages=[{"role": "user", "content": basicPrompt + prompt}]
		)

		message = response.choices[0].message.content

		ChatAnswer.objects.create(
			device=device,
			prompt=prompt,
			answer=message,
		)

		return Response({"Response": message})
