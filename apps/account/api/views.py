from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.serializers import TokenBlacklistSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            serializer = TokenBlacklistSerializer(data=request.data)
            if serializer.is_valid():
                content = {'message': 'Successfully logged out'}
                return Response(content, status=status.HTTP_205_RESET_CONTENT)            
        except Exception as e:
            print(e)  # TODO log exception
        return Response(status=status.HTTP_400_BAD_REQUEST)

