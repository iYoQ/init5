from rest_framework import routers
from users.viewsets import UserViewSet

router = routers.DefaultRouter()

router.register('users', UserViewSet)