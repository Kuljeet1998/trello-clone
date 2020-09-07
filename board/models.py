from django.db import models
from django.contrib.auth.models import User
from common.models import UUIDTimeStamp,Attachment,Enum
# Create your models here.

class Board(UUIDTimeStamp, Enum):
	creator=models.ForeignKey(User,related_name="boards", on_delete=models.CASCADE)
	members=models.ManyToManyField(User,related_name="member_in_boards",null=True,blank=True)

	def __str__(self):
		return self.title


class List(UUIDTimeStamp, Enum):
	board=models.ForeignKey(Board,related_name="lists",on_delete=models.CASCADE)
	order=models.PositiveIntegerField(null=False)

	def __str__(self):
		return self.title

	class Meta:
		ordering=['order']

class Card(UUIDTimeStamp, Enum):
	list=models.ForeignKey(List,related_name="cards",on_delete=models.CASCADE)
	attachments=models.ManyToManyField(Attachment,related_name="cards",null=True,blank=True)
	order=models.PositiveIntegerField(null=False)

	def __str__(self):
		return self.title

	class Meta:
		ordering=['order']


class Comment(UUIDTimeStamp):
	message=models.TextField()
	card=models.ForeignKey(Card,related_name="comments",on_delete=models.CASCADE)
	user=models.ForeignKey(User,related_name="comments", on_delete=models.CASCADE)

	def __str__(self):
		return str(self.id)