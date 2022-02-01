from rest_framework import generics
from .models import MailingList
from .serializers import MailingListSerializer


class Subscribe(generics.ListCreateAPIView):
    model = MailingList
    serializer_class = MailingListSerializer
