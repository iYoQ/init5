from rest_framework import generics
from rest_framework import filters
from .models import MailingList
from .serializers import MailingListSerializer
from ..general.paginations import LargePagination
from rest_framework.permissions import IsAdminUser


class Subscribe(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    model = MailingList
    serializer_class = MailingListSerializer
    pagination_class = LargePagination
    filter_backends = [filters.SearchFilter]
    queryset = MailingList.objects.all()
    search_fields = ['email']
