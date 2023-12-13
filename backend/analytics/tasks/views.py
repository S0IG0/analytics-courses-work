from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from files.views import SmallResultsSetPagination
from tasks.filters import TaskFilter, SupplyFilter
from tasks.models import Task, Supply
from tasks.serializers import TaskSerializer, AnalyticSerializer, ShortTaskSerializer, SupplySerializer
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
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = TaskFilter


class StartAnalytic(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        analytic = AnalyticSerializer(data=request.data)
        analytic.is_valid(raise_exception=True)
        file_id = analytic.validated_data["file_id"]
        task = Task.objects.create(delivery=analytic.validated_data["delivery"])
        analytics.apply_async((task.pk, file_id,), )
        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)


class SupplyList(ListCreateAPIView):
    queryset = Supply.objects.all().order_by('name', 'date')
    serializer_class = SupplySerializer
    permission_classes = [AllowAny, ]
    pagination_class = SmallResultsSetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = SupplyFilter

