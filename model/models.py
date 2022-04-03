from django.db import models


PLATFORM_CHOICES = [
    ('tensorrt_plan', 'tensorrt_plan'),
    ('pytorch_libtorch', 'pytorch_libtorch'),
    ('onnxruntime_onnx', 'onnxruntime_onnx'),
    ('tensorflow', 'tensorflow'),
    ('ensemble', 'ensemble'),
    ('', 'none'),
]

BACKEND_CHOICES = [
    ('tensorrt', 'tensorrt'),
    ('pytorch', 'pytorch'),
    ('onnxruntime', 'onnxruntime'),
    ('tensorflow_graphdef', 'tensorflow_graphdef'),
    ('tensorflow_savedmodel', 'tensorflow_savedmodel'),
]

# Create your models here.
class Model(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    platform = models.CharField(choices=PLATFORM_CHOICES, max_length=100)
    backend = models.CharField(choices=BACKEND_CHOICES, max_length=100)
    inputs = models.JSONField()
    outputs = models.JSONField()
    max_batch_size = models.PositiveSmallIntegerField(default=0)