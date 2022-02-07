from rest_framework import generics
from rest_framework import filters
from .models import MailingList
from .serializers import MailingListSerializer
from ..general.paginations import LargePagination
from rest_framework.permissions import IsAdminUser, AllowAny


class Subscribe(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [AllowAny]
    model = MailingList
    serializer_class = MailingListSerializer
    queryset = MailingList.objects.all()
    pagination_class = LargePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['email']

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        elif self.request.method in ['GET', 'DELETE']:
            self.permission_classes = [IsAdminUser]

        return super().get_permissions()
