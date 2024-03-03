from django.shortcuts import render
import jwt
from django.contrib.auth import authenticate
from account.models import Account
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer

from rest_framework_simplejwt.tokens import RefreshToken

from account.producer import produce_create_event, produce_delete_event, produce_role_changed_event, produce_update_event
from .serializers import CreateUserSerializer, UserDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

    
class AccountView(APIView):
    '''
        /accounts
    '''
    
    def get_serializer_class(self):
        if self.request.method == 'POST' and not 'pk' in self.kwargs:
            return CreateUserSerializer
        return UserDetailSerializer
    
    def get(self, request, pk=None):
        if pk:
            user = Account.objects.get(uuid=pk)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(user)
        else:
            users = Account.objects.all()
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            produce_create_event(account)
            return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        account = Account.objects.get(uuid=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=account, data=request.data, partial=True)
        if serializer.is_valid():
            account = serializer.save()
            if 'role' in serializer.validated_data:
                produce_role_changed_event(account)
            produce_update_event(account)
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = Account.objects.get(uuid=pk)
        user.delete()
        produce_delete_event(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
