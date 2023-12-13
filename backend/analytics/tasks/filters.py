from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from tasks.models import Task, Supply


class TaskFilter(FilterSet):
    class Meta:
        model = Task
        fields = {
            'delivery': ['exact'],
        }


class SupplyFilter(FilterSet):
    task = CharFilter(field_name='task__pk', lookup_expr='icontains')

    class Meta:
        model = Supply
        fields = ['task']
