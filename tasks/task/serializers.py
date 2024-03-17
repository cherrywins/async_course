from account.models import Account
from rest_framework import serializers
import random
from task.models import Task

class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('description')

    def create(self, validated_data):
        assignee_ids = Account.objects.exclude(role__in=['manager', 'admin']).values_list('id', flat=True)
        task = Task.objects.create(
            description=validated_data['description'],
            assignee_id=int(random.choice(assignee_ids)),
            status='assigned', 
        )
        return task
    

class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('description')
    
    def update(self, validated_data):
        task = self.instance
        task.update(**validated_data)
        return task
