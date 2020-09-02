from django.contrib.auth.models import *
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from rest_framework.response import Response
from django.conf import settings
from rest_framework.authtoken.models import Token

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_token(sender,instance,**kwargs):
	# print(instance)
	token=Token.objects.filter(user=instance).exists()
	if token==False:
		Token.objects.create(user=instance)
	