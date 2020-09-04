from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import MultiPartParser

# Create your views here.
class AttachmentViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	parser_classes=[MultiPartParser]
	
	queryset=Attachment.objects.all()
	serializer_class=AttachmentSerializer

	def list(self,request):
		queryset = Attachment.objects.all()
		serializer=AttachmentSerializer(queryset,many=True,context={'request': request})
		return Response(serializer.data,status=200)

	def post(self,request,format=None):
		file_obj=request.data['document']
		serializer=AttachmentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data,status=201)
		return Response(serializer.data,status=204)