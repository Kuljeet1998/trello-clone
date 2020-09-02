from .models import *
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model=User
		fields=['id','first_name','last_name','email','username']

class BoardSerializer(serializers.ModelSerializer):
	creator_details=UserSerializer(read_only=True,source="creator")
	member_details=UserSerializer(read_only=True,many=True,source="members")
	
	class Meta:
		model=Board
		fields='__all__'

class ListSerializer(serializers.ModelSerializer):
	class Meta:
		model=List
		fields='__all__'

class CardSerializer(serializers.ModelSerializer):
	class Meta:
		model=Card
		fields='__all__'

class CommentSerializer(serializers.ModelSerializer):
	class Meta:
		model=Comment
		fields='__all__'