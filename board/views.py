from django.shortcuts import render, get_object_or_404
from .models import *
from .serializers import *
from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):

	queryset=User.objects.all()
	serializer_class=UserSerializer
	http_method_names = ['get', 'put']


class BoardViewSet(viewsets.ModelViewSet):
	filter_backends = [filters.SearchFilter]
	search_fields = ['title']

	queryset=Board.objects.all()
	serializer_class=BoardSerializer

class ListViewSet(viewsets.ModelViewSet):
	filter_backends = [filters.SearchFilter]
	search_fields = ['title']

	queryset=List.objects.all()
	serializer_class=ListSerializer

class CardViewSet(viewsets.ModelViewSet):
	filter_backends = [filters.SearchFilter]
	search_fields = ['title']

	queryset=Card.objects.all()
	serializer_class=CardSerializer

class CommentViewSet(viewsets.ModelViewSet):

	queryset=Comment.objects.all()
	serializer_class=CommentSerializer

class OrderLists(APIView):

	def post(self,request):
		request_data=request.data
		ordered_list=request_data.get('ordered_lists')
		board_id=request_data.get('board_id')
		i=1

		for list_id in ordered_list:
			try:
				is_present=List.objects.filter(id=list_id).exists()
			except:
				is_present=False
			if is_present is False:
				return Response('ID does not exist!')

		for list_id in ordered_list:
			list_object=List.objects.get(id=list_id)
			serializer=ListSerializer(data={'board_id':board_id}, instance=list_object, partial=True)
			if serializer.is_valid():
				list_object.order=i
				i=i+1
				serializer.save()
		return Response("Done")


class OrderCards(APIView):

	def post(self,request):
		request_data=request.data
		ordered_cards=request_data.get('ordered_cards')
		list_id=request_data.get('list_id')
		i=1

		for card_id in ordered_cards:
			try:
				is_present=Card.objects.filter(id=card_id).exists()
			except:
				is_present=False
			if is_present is False:
				return Response('ID does not exist!')

		for card_id in ordered_cards:
			card_object=Card.objects.get(id=card_id)
			serializer=CardSerializer(data={'list_id':list_id}, instance=card_object, partial=True)
			if serializer.is_valid():
				card_object.order=i
				i=i+1
				serializer.save()
		return Response("Done")

# class MeAPI(APIView):

# 	def get(self,request):
# 		user=self.request.user
# 		is_user=User.objects.filter(id=user.id).exists()
# 		if is_user:
# 			user=User.objects.get(id=user.id)
# 			serializer=UserSerializer(user)
# 			return Response(serializer.data,status=201)