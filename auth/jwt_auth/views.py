from django.shortcuts import render
import jwt
from django.contrib.auth import authenticate
from account.models import Account
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CreateUserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


class TokenView(APIView):
    '''
        /token
    '''

    def post(self, request):
        '''
            Request by other service to get the token
        '''
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            account = Account.objects.filter(email=serializer.validated_data['email']).first()
            if not account:
                return Response({"detail": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
            user = authenticate(request, username=account.uuid, password=serializer.validated_data['password'])
            if user is not None:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    })
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class InfoView(APIView):
    '''
        /account_info
        Request by other service to get the user's information
    '''
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # The user's information is already available through request.user
        # thanks to the IsAuthenticated permission class
        user = request.user
        user_info = {
            'id': user.uuid,
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'role': user.role,
            
        }
        return Response(user_info)
