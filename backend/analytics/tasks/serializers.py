from rest_framework import serializers

from files.serializers import FileSerializer
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = '__all__'

    @staticmethod
    def get_files(task):
        files = task.files.all()
        serializer = FileSerializer(files, many=True)
        return serializer.data


class ShortTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'status'
        )


class AnalyticSerializer(serializers.Serializer):
    file_id = serializers.IntegerField(required=True)
    delivery = serializers.BooleanField(required=False, default=False)
