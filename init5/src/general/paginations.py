from rest_framework.pagination import CursorPagination
from rest_framework.response import Response


class CustomResponsePagination(CursorPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'results': data
        })


class UserPagination(CustomResponsePagination):
    page_size = 20
    cursor_query_param = 'page'
    ordering = 'rating'


class PostPagination(CustomResponsePagination):
    page_size = 10
    cursor_query_param = 'page'
    ordering = '-date_create'
