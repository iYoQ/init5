from rest_framework import routers
from users.viewsets import UserViewSet
from posts.viewsets import *

router = routers.DefaultRouter()

router.register('users', UserViewSet)
router.register('articles', ArticleViewSet)
router.register('news', NewsViewSet)