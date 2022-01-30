from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomResponsePagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
                'count': self.page.paginator.count,
            },
            'results': data
        })


class UserPagination(CustomResponsePagination):
    page_size = 20
    page_query_param = 'page'
    ordering = '-rating'


class PostPagination(CustomResponsePagination):
    page_size = 10
    page_query_param = 'page'
    ordering = '-date_create'


class CommentsPagination(CustomResponsePagination):
    page_size = 15
    page_query_param = 'page'
    ordering = '-date_create'
