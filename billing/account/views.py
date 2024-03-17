from django.shortcuts import render
import requests
from account.models import Account
from account.serializers import LoginSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

def get_account_info(token: str):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json' # This is common for APIs expecting JSON data
    }
    url = 'http://127.0.0.1:8000/account_info/'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return {'status': 'ok', 'data': response.json()}
    else:
        return {'status': 'error', 'data':f'Request failed with status code {response.status_code}.'}

class LoginView(APIView):
    '''
        /billing_login
    '''

    def post(self, request):
        '''
            Request by other service to get the token
        '''
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            
            response = requests.post('http://127.0.0.1:8000/token/', data={
                'email': serializer.data['email'],
                'password': serializer.data['password'],
            })
            if response.status_code == 200:
                token = response.json().get('access')
                refresh_token = response.json().get('refresh')
                response = get_account_info(token)
                if response['status'] == 'ok':
                    account_info = response['data']
                    account, _ = Account.objects.get_or_create(
                        uuid=account_info['id'],
                    )
                    account.username=account_info['username']
                    account.email=account_info['email']
                    account.name=account_info['name']
                    account.role=account_info['role']
                    account.token=token
                    account.refresh_token=refresh_token
                    account.save()
                    return Response({"status": 'success'}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
