from rest_framework import serializers

from files.serializers import FileSerializer
from tasks.models import Task, Supply, Graph


class GraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Graph
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True)
    graphs = GraphSerializer(many=True)

    class Meta:
        model = Task
        fields = '__all__'


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


class SupplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Supply
        fields = "__all__"
