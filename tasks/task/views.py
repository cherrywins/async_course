from django.shortcuts import get_object_or_404
from account.models import Account
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import random
from rest_framework import viewsets

from task.models import Task
from task.utils import reassign_tasks
from .serializers import CreateTaskSerializer, TaskDetailSerializer
from rest_framework.decorators import action
import uuid
from .producer import produce_task_assign_event, produce_task_create_event, produce_task_complete_event
    
class TaskViewSet(viewsets.ViewSet):
    '''
        /tasks
    '''
    
    def get_serializer_class(self):
        if self.request.path.endswith('/reassigne_tasks/'):
            return None
        if self.request.method == 'POST' and not 'pk' in self.kwargs:
            return CreateTaskSerializer
        return TaskDetailSerializer
    
    def get(self, request, pk=None):
        if pk:
            task = get_object_or_404(Task, id=pk)
            serializer_class = self.get_serializer_class()
            serializer = serializer_class(task)
        else:
            status_filter = request.query_params.get('status', None)
            assignee_filter = request.query_params.get('assignee', None)  #email
            
            tasks = Task.objects.all()
            if status_filter:
                tasks = tasks.filter(status=status_filter)
            if assignee_filter:
                tasks = tasks.filter(assignee__email=assignee_filter)

            serializer_class = self.get_serializer_class()
            serializer = serializer_class(tasks, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            produce_task_create_event(task)
            produce_task_assign_event(task)
            return Response(
                {"task": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        task = Account.objects.get(uuid=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(instance=task, data=request.data, partial=True)
        if serializer.is_valid():
            task = serializer.save()
            return Response({"user": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"])
    def reassigne_tasks(self, request):
        reassign_tasks()
        return Response({"message": "Tasks reassigned successfully."})
    
    
    @action(detail=True, methods=["post"])
    def complete_task(self, request):
        task: Task = self.get_object()
        task.status = 'completed'
        if not task.uuid:
            task.uuid = uuid.uuid4()
        task.save()
        produce_task_complete_event(task)
        return Response(status=status.HTTP_200_OK)
    
