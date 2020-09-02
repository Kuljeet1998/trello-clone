from .models import *
from rest_framework import serializers

class AttachmentSerializer(serializers.ModelSerializer):

	class Meta:
		model=Attachment
		fields='__all__'