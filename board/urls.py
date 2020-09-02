from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'boards', BoardViewSet)
router.register(r'lists', ListViewSet)
router.register(r'cards', CardViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns=[
    path('me/',MeAPI.as_view()),
]
urlpatterns +=router.urls