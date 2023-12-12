from rest_framework import serializers

from files.models import File, Macaroni


class FileSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = '__all__'

    @staticmethod
    def get_name(obj):
        return obj.file.name.split('/')[-1]


class MacaroniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Macaroni
        fields = '__all__'
