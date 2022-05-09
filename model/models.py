from django.db import models
from django.core.exceptions import ValidationError


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

DATA_TYPE_CHOICES = [
    ('TYPE_STRING', 'TYPE_STRING'),
    ('TYPE_BOOL', 'TYPE_BOOL'),
    ('TYPE_UINT8', 'TYPE_UINT8'),
    ('TYPE_UINT16', 'TYPE_UINT16'),
    ('TYPE_UINT32', 'TYPE_UINT32'),
    ('TYPE_UINT64', 'TYPE_UINT64'),
    ('TYPE_INT8', 'TYPE_INT8'),
    ('TYPE_INT16', 'TYPE_INT16'),
    ('TYPE_INT32', 'TYPE_INT32'),
    ('TYPE_INT64', 'TYPE_INT64'),
    ('TYPE_FP16', 'TYPE_FP16'),
    ('TYPE_FP32', 'TYPE_FP32'),
    ('TYPE_FP64', 'TYPE_FP64'),
]

def validate_dims(value):
    if type(value) == list and len(value) > 0:
        for v in value:
            if type(v) != int or v < -1 or v == 0:
                break
        else:
            return
    raise ValidationError('dims must be non-empty list of positive integers and -1.')

# Create your models here.
class Model(models.Model):
    name = models.CharField(unique=True, max_length=100)
    platform = models.CharField(choices=PLATFORM_CHOICES, max_length=100)
    backend = models.CharField(choices=BACKEND_CHOICES, max_length=100)
    max_batch_size = models.PositiveSmallIntegerField(default=0)

class Input(models.Model):
    name = models.CharField(max_length=100)
    data_type = models.CharField(choices=DATA_TYPE_CHOICES, max_length=20)
    dims = models.JSONField(validators=[validate_dims])
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='inputs')

class Output(models.Model):
    name = models.CharField(max_length=100)
    data_type = models.CharField(choices=DATA_TYPE_CHOICES, max_length=20)
    dims = models.JSONField(validators=[validate_dims])
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='outputs')

class Version(models.Model):
    version = models.PositiveSmallIntegerField()
    model_file = models.FileField(upload_to='model_files/', null=True)
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='versions')