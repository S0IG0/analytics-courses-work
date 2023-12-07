from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from files.models import File


class FileFilter(FilterSet):
    file = CharFilter(method='filter_file')

    class Meta:
        model = File
        fields = ['file']

    @staticmethod
    def filter_file(queryset, name, value):
        return queryset.filter(file__icontains=value)
