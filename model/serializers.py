from rest_framework import serializers
from .models import Model, Version, Input, Output


class InputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input
        exclude = ['id', 'model']

class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output
        exclude = ['id', 'model']

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        exclude = ['id', 'model']
        read_only_fields = ['version']

class ModelSerializer(serializers.ModelSerializer):
    inputs = InputSerializer(many=True, read_only=True)
    outputs = OutputSerializer(many=True, read_only=True)
    versions = VersionSerializer(many=True, read_only=True)

    class Meta:
        model = Model
        exclude = ['id']