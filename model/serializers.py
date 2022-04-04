from rest_framework import serializers
from .models import Model, Version


class ModelSerializer(serializers.ModelSerializer):
    versions = serializers.SlugRelatedField(many=True, read_only=True, slug_field='version')

    class Meta:
        model = Model
        fields = '__all__'

class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        exclude = ['id', 'model']
        read_only_fields = ['version']