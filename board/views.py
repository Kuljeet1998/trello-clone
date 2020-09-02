from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	# permission_classes = (IsAuthenticated,)

	queryset=User.objects.all()
	serializer_class=UserSerializer

	def create(self,request):
		serializer=UserSerializer(data=request.data)
		if serializer.is_valid():
			email=request.POST.get('email')
			try:
				user = User.objects.get(email=email)
			except User.DoesNotExist:
				user = None

			if user is not None:
				return HttpResponse("Email already exists")
			else:
				serializer.save()
				return Response(serializer.data,status=201)
		return Response(serializer.errors,status=204)

class BoardViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	filter_backends = [filters.SearchFilter]
	search_fields = ['title']

	queryset=Board.objects.all()
	serializer_class=BoardSerializer

class ListViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	filter_backends = [filters.SearchFilter]
	search_fields = ['title']

	queryset=List.objects.all()
	serializer_class=ListSerializer

class CardViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)
	filter_backends = [filters.SearchFilter]
	search_fields = ['title']

	queryset=Card.objects.all()
	serializer_class=CardSerializer

class CommentViewSet(viewsets.ModelViewSet):
	authentication_classes = (TokenAuthentication,)

	queryset=Comment.objects.all()
	serializer_class=CommentSerializer


class MeAPI(APIView):
	authentication_classes = (TokenAuthentication,)

	def get(self,request):
		user=self.request.user
		is_user=User.objects.filter(id=user.id).exists()
		if is_user:
			user=User.objects.get(id=user.id)
			serializer=UserSerializer(user)
			return Response(serializer.data,status=201)