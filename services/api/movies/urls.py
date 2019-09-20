from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'movies', MovieViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'top', TopViewSet)

urlpatterns = router.urls