from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from tasks.models import Task
from tasks.serializers import TaskSerializer, AnalyticSerializer
from tasks.tasks import analytics


class RetrieveTask(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny, ]


class StartAnalytic(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        analytic = AnalyticSerializer(data=request.data)
        analytic.is_valid(raise_exception=True)
        file_id = analytic.validated_data["file_id"]
        task = Task.objects.create()
        analytics.apply_async((task.pk, file_id,), )
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
