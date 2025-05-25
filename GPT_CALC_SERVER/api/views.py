from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from openai import OpenAI
import os


# Create your views here.

class ChatGPTView(APIView):

	def post(self, request):
		client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

		response = client.chat.completions.create(
			model="gpt-4",
			messages=[{"role": "user", "content": "Czym jest krowa?"}]
		)

		message = response.choices[0].message.content

		return Response({"Response": message})