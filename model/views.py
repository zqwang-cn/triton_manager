from rest_framework import generics
from .models import Model
from .serializers import ModelSerializer


# Create your views here.
class ModelList(generics.ListCreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer

class ModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer