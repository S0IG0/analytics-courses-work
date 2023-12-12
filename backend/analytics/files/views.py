import csv

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from files.filters import FileFilter, MacaroniFilter
from files.models import File, Macaroni
from files.serializers import FileSerializer, MacaroniSerializer
from files.tasks import save_rows


class FileUploadView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        file_serializer = FileSerializer(data=request.data)

        if file_serializer.is_valid():
            file_instance = file_serializer.save()
            save_rows.apply_async((file_instance.pk,), )
            return Response(file_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


class FileList(ListCreateAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [AllowAny, ]
    pagination_class = SmallResultsSetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = FileFilter


class MacaroniList(ListCreateAPIView):
    queryset = Macaroni.objects.all()
    serializer_class = MacaroniSerializer
    permission_classes = [AllowAny, ]
    pagination_class = SmallResultsSetPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = MacaroniFilter
