from account.models import Account
from rest_framework import serializers

from task.models import Task

class CreateTaskSerializer(serializers.ModelSerializer):
    assignee_email = serializers.CharField(write_only=True, required=True)
    assignee = serializers.StringRelatedField(source='assignee.email', read_only=True)
    
    class Meta:
        model = Task
        fields = ('description', 'assignee_email', 'assignee')

    def create(self, validated_data):
        account = Account.objects.filter(email=validated_data['assignee_email']).first()
        if not account:
            raise serializers.ValidationError({'email': 'User with this email does not exists'})
        task = Task.objects.create(
            description=validated_data['description'],
            assignee=account,
            status='assigned'
        )
        return task
    

class TaskDetailSerializer(serializers.ModelSerializer):
    assignee_email = serializers.StringRelatedField(source='assignee.email', read_only=True)
    assignee_name = serializers.StringRelatedField(source='assignee.name', read_only=True)
    class Meta:
        model = Task
        fields = ('description', 'status', 'assignee_email', 'assignee_name')
    
    def update(self, validated_data):
        task = self.instance
        task.update(**validated_data)
        return task
