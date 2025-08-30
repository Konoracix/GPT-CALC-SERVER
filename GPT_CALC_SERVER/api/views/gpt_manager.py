from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from openai import OpenAI
from rest_framework.exceptions import NotFound
from drf_yasg.utils import swagger_auto_schema
import os
from rest_framework import status
from api.models import Device, ChatAnswer
from api.serializers import PromptSerializer, ChatAnswerSerializer
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from api.permissions import IsDeviceAuthenticated



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
	@action(detail=True, methods=["POST"], serializer_class=PromptSerializer, permission_classes=[IsDeviceAuthenticated])
	def answer(self, request, pk: int):
		serializer = PromptSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
		try:
			device = Device.objects.get(id=pk)
			device.number_of_requests += 1
			device.save()
		except:
			raise NotFound(detail=f'Device with id: {pk} Not Found')
		
		prompt = serializer.validated_data["prompt"]

		basicPrompt = """Jesteś asystentem pomagającym uczniom przy sciąganiu.
			Twoje odpowiedzi powinny być jak najbardziej zwięzłe jak potrafisz i powinny zawierać tylko kluczowe informacje. 
			Najlepiej żeby zawierały się maksymalnie w kilku słowach. Jeżeli pytasz o wzór powinieneś napisać sam wzór. 
			Nie formatuj tekstu. Zwróć prostego jednolinijkowego stringa. 
			Jeżeli w odpowiedzi występuje ułamek dziesiętny podaj odpowiedz w ułamku zwykłym Pytanie ucznia brzmi tak: """

		response = client.chat.completions.create(
			model="o3-mini-2025-01-31",
			messages=[{"role": "user", "content": (basicPrompt + prompt)}]
		)
	
		#sqrt(3)tg(alfa)=2sin(alfa). Jaka jest wartość cos(alfa). wiedząc że Kąt alfa jest ostry

		message = response.choices[0].message.content

		ChatAnswer.objects.create(
			device=device,
			prompt=prompt,
			answer=message,
		)


		return Response({"Response": message})



# # Create your views here.
# @api_view(['POST'])
# def sendRequest(request, id):
	

# @api_view(['GET', 'POST'])
# def getAllDevices(request):
# 	if request.method == 'GET':
# 		devices = Device.objects.filter(deleted_at=None)
# 		serializer = DeviceSerializer(devices, many=True)
# 		return Response(serializer.data)
	
# 	if request.method == 'POST':
# 		serializer = DeviceSerializer(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		return Response(serializer.errors)

# @api_view(['GET'])
# def getOneDevice(request, id):
# 	try:
# 		device = Device.objects.get(id=id)
# 		serialier = DeviceSerializer(device)
# 		return Response(serialier.data)
# 	except:
# 		raise NotFound(detail=f'Device with id: {id} Not Found')