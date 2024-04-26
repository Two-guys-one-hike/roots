import logging

from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.serializers import TokenBlacklistSerializer

logger = logging.getLogger(__name__)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            serializer = TokenBlacklistSerializer(data=request.data)
            if serializer.is_valid():
                return Response(status=status.HTTP_205_RESET_CONTENT)
            else:
                logger.warning(f'{self.__class__.__name__} - data not valid - {request.data}')
        except Exception as e:
            logger.warning(f'{self.__class__.__name__} - validation error - {e}')
        return Response(status=status.HTTP_400_BAD_REQUEST)
