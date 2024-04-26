from django.shortcuts import render

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        try:
            serializer = TokenBlacklistSerializer(request.data)
            serializer.data
            content = {'message': 'Successfully logged out'}
            return Response(content)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
