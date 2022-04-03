from rest_framework import serializers


OPERATION_CHOICES = [
    'create',
    'remove',
    'start',
    'stop',
]

class OperationSerializer(serializers.Serializer):
    op = serializers.ChoiceField(OPERATION_CHOICES)