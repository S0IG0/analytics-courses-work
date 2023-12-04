from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task
from tasks.serializers import TaskSerializer
from tasks.tasks import analytics


class RetrieveTask(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny, ]


class StartAnalytic(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        task = Task.objects.create()
        analytics.apply_async((task.pk,), )
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
