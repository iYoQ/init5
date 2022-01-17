from rest_framework import routers
from src.users.viewsets import UserViewSet
from src.news.viewsets import NewsViewSet
from src.articles.viewsets import ArticleViewSet
from src.comments.viewsets import ArticleCommentViewSet, NewsCommentViewSet


router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='users')
router.register('articles', ArticleViewSet, basename='articles')
router.register('news', NewsViewSet, basename='news')
router.register('articles_comments', ArticleCommentViewSet, basename='articles_comments')
router.register('news_comments', NewsCommentViewSet, basename='news_comments')