from account.models import Account
from rest_framework import serializers

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'password', 'name', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if Account.objects.filter(email=validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'User with this email already exists'})
        if validated_data['role'] not in ['admin', 'user', 'manager']:
            raise serializers.ValidationError({'role': 'Role must be either admin or user or manager'})
        user = Account.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            username=validated_data['email'],
            role=validated_data['role'],
            password=validated_data['password'],
        )
        return user
    

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'name', 'role')
        
    def validate_role(self, value):
        if value not in ['admin', 'user', 'manager']:
            raise serializers.ValidationError({'role': 'Role must be either admin or user or manager'})
        return value
    
    def validate_email(self, value):
        if Account.objects.filter(email=value).exists():
            raise serializers.ValidationError({'email': 'User with this email already exists'})
    
    def update(self, validated_data):
        user = self.instance
        
        user.update(
            email=validated_data['email'],
            name=validated_data['name'],
            role=validated_data['role'],
        )
        return user
