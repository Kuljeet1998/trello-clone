from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r'attachments', AttachmentViewSet, basename="attachments")

urlpatterns = router.urls +static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)