from .models import *
from rest_framework import serializers
from common.serializers import AttachmentSerializer
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

class BoardDetailSerializer(serializers.ModelSerializer):
	list_details=ListSerializer(read_only=True,many=True,source="lists")

	class Meta:
		model=Board
		fields='__all__'

class CardDetailSerializer(serializers.ModelSerializer):
	attachment_details=AttachmentSerializer(read_only=True,many=True,source="attachments")
	comment_details=CommentSerializer(read_only=True,many=True,source="comments")

	class Meta:
		model=Card
		fields="__all__"

class ListDetailSerializer(serializers.ModelSerializer):
	card_details=CardSerializer(read_only=True,many=True,source="cards")

	class Meta:
		model=List
		fields="__all__"