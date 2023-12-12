from django_filters import CharFilter
from django_filters.rest_framework import FilterSet

from files.models import File, Macaroni


class FileFilter(FilterSet):
    file = CharFilter(method='filter_file')

    class Meta:
        model = File
        fields = ['file']

    @staticmethod
    def filter_file(queryset, name, value):
        return queryset.filter(file__icontains=value)


class MacaroniFilter(FilterSet):
    file = CharFilter(field_name='file__pk', lookup_expr='icontains')

    class Meta:
        model = Macaroni
        fields = ['file']
