from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers

router=routers.SimpleRouter()
router.register(r'users', UserViewSet,  basename="users")
router.register(r'boards', BoardViewSet, basename="boards")
router.register(r'lists', ListViewSet, basename="lists")
router.register(r'cards', CardViewSet, basename="cards")
router.register(r'comments', CommentViewSet, basename="comments")

urlpatterns=[
    path('order_lists/',OrderLists.as_view()),
    path('order_cards/',OrderCards.as_view())
]


urlpatterns +=router.urls