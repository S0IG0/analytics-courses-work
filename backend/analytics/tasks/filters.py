from django_filters import rest_framework as filters

from tasks.models import Task


class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'delivery': ['exact'],
        }
