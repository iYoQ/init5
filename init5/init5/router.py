from rest_framework import routers
from users.viewsets import ProfileViewSet

router = routers.DefaultRouter()

router.register('', ProfileViewSet)