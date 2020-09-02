from django.db import models
import uuid
# Create your models here.

class UUID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Timestamp(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDTimeStamp(UUID, Timestamp):
    pass

    class Meta:
        abstract = True


class Enum(models.Model):
	title=models.CharField(max_length=20)
	description=models.TextField(blank=True, null=True)

	class Meta:
		abstract=True


class Attachment(UUIDTimeStamp):
	document=models.FileField(upload_to="documents/")

	@property
	def file_url(self):
		return self.document.url
	
	def __str__(self):
		return str(self.file_url)