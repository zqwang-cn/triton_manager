from django.shortcuts import get_object_or_404 
from rest_framework import generics
from .models import Model, Version
from .serializers import ModelSerializer, VersionSerializer


# Create your views here.
class ModelList(generics.ListCreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

class ModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

class VersionList(generics.ListCreateAPIView):
    serializer_class = VersionSerializer

    def get_queryset(self):
        model = get_object_or_404(Model, name=self.kwargs['name'])
        return model.versions
    
    def perform_create(self, serializer):
        model = get_object_or_404(Model, name=self.kwargs['name'])
        first = model.versions.order_by('-version').first()
        serializer.validated_data['model'] = model
        serializer.validated_data['version'] = 1 if first is None else first.version + 1
        serializer.save()

class VersionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VersionSerializer

    def get_object(self):
        name = self.kwargs['name']
        version = self.kwargs['version']
        return get_object_or_404(Version, model=name, version=version)
