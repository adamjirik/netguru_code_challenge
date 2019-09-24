from rest_framework import routers
from rest_framework.schemas import get_schema_view
from .views import *
from django.urls import path

router = routers.SimpleRouter()
router.register(r'movies', MovieViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'top', TopViewSet)

urlpatterns = [
    path('', get_schema_view(
    title="Movie Database",
    description="A movie database to save movies and make comments",
    version="1.0.0"),
    name="openapi-schema"
)
] +router.urls