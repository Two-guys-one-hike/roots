import logging

from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.serializers import TokenBlacklistSerializer

logger = logging.getLogger(__name__)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        data = dict()
        try:
            serializer = TokenBlacklistSerializer(data=request.data)
            if serializer.is_valid():
                return Response(status=status.HTTP_205_RESET_CONTENT)
            else:
                data = {'error': 'Refresh token not provided'}
                logger.warning(
                    f'{self.__class__.__name__} - refresh token not provided - {request.data}'
                )
        except Exception as e:
            data = {'error': str(e)}
            logger.warning(f'{self.__class__.__name__} - validation error - {e}')
        return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'is_staff': request.user.is_staff,
        }
        return Response(data=user, status=status.HTTP_200_OK)
