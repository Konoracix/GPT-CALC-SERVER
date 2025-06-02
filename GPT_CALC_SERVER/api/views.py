from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from openai import OpenAI
from rest_framework.decorators import api_view
from api.serializers import DeviceSerializer 
from rest_framework.exceptions import NotFound
import os
from api.models import Device

# Create your views here.
@api_view(['POST'])
def sendRequest(request, id):
	client = OpenAI(api_key=os.getenv("OPENAI_KEY"))
	try:
		device = Device.objects.get(id=id)
		device.number_of_requests += 1
		device.save()
	except:
		raise NotFound(detail=f'Device with id: {id} Not Found')

	prompt = request.data.get("prompt")

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

	return Response({"Response": message})

@api_view(['GET', 'POST'])
def getAllDevices(request):
	if request.method == 'GET':
		devices = Device.objects.filter(deleted_at=None)
		serializer = DeviceSerializer(devices, many=True)
		return Response(serializer.data)
	
	if request.method == 'POST':
		serializer = DeviceSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors)

@api_view(['GET'])
def getOneDevice(request, id):
	try:
		device = Device.objects.get(id=id)
		serialier = DeviceSerializer(device)
		return Response(serialier.data)
	except:
		raise NotFound(detail=f'Device with id: {id} Not Found')