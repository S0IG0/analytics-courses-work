from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from files.views import SmallResultsSetPagination
from tasks.models import Task
from tasks.serializers import TaskSerializer, AnalyticSerializer, ShortTaskSerializer
from tasks.tasks import analytics


class TaskRetrieve(RetrieveAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny, ]


class TaskList(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = ShortTaskSerializer
    permission_classes = [AllowAny, ]
    pagination_class = SmallResultsSetPagination


class StartAnalytic(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        analytic = AnalyticSerializer(data=request.data)
        analytic.is_valid(raise_exception=True)
        file_id = analytic.validated_data["file_id"]
        task = Task.objects.create()
        analytics.apply_async((task.pk, file_id,), )
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
