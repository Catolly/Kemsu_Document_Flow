from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

class Pagination(LimitOffsetPagination):

    def get_paginated_response(self, data):
        return Response({
            'studentsAmount':data['studentsAmount'],
            'students':data['students']
        }, status.HTTP_200_OK)