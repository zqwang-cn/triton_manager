import os
import shutil

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from model.models import Model
from .serializers import OPERATION_CHOICES, OperationSerializer

REPO_DIR = '/root/repo'

def create():
    remove()
    os.mkdir(REPO_DIR)

    for model in Model.objects.all():
        model_dir = os.path.join(REPO_DIR, model.name)
        os.mkdir(model_dir)

def remove():
    if os.path.exists(REPO_DIR):
        shutil.rmtree(REPO_DIR)

def start():
    pass

def stop():
    pass

# Create your views here.
class OperationList(APIView):
    serializer_class = OperationSerializer
    
    def get(self, request):
        return Response(OPERATION_CHOICES)
    
    def post(self, request):
        serializer = OperationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"msg": "Input not valid."}, status=status.HTTP_400_BAD_REQUEST)

        op = serializer.data['op']
        if op == 'create':
            create()
        elif op == 'remove':
            remove()
        elif op == 'start':
            start()
        elif op == 'stop':
            stop()
        else:
            return Response({"msg": "Operation not exists."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"msg": "Success."})
    