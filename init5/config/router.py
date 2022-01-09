from rest_framework import routers
from src.users.viewsets import UserViewSet
from src.posts.viewsets import (
    ArticleViewSet, 
    NewsViewSet
)


router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('articles', ArticleViewSet, basename='articles')
router.register('news', NewsViewSet, basename='news')
