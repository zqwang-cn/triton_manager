import os
import shutil
import subprocess
import jinja2

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from model.models import Model
from .serializers import OPERATION_CHOICES, OperationSerializer

REPO_DIR = '/root/repo'
TRITON_START_COMMAND = 'tritonserver --model-repository {}'
TEMPLATE_DIR = '/root/templates'
TEMPLATE_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

triton_process = None

def create_model(model):
    model_dir = os.path.join(REPO_DIR, model.name)
    if not os.path.exists(model_dir):
        os.mkdir(model_dir)

    template = TEMPLATE_ENV.get_template('config.pbtxt')
    s = template.render(model=model)
    with open(os.path.join(model_dir, 'config.pbtxt'), 'w') as f:
        f.write(s)

def create():
    msg = remove()
    if msg is not None:
        return msg
    os.mkdir(REPO_DIR)

    for model in Model.objects.all():
        create_model(model)

def remove():
    if triton_process is not None and triton_process.poll() is None:
        return 'Triton still running.'

    if os.path.exists(REPO_DIR):
        shutil.rmtree(REPO_DIR)

def start():
    global triton_process
    if triton_process is not None and triton_process.poll() is None:
        return 'Triton already running.'

    if not os.path.exists(REPO_DIR):
        return 'Model dir not exists.'

    cmd = TRITON_START_COMMAND.format(REPO_DIR)
    triton_process = subprocess.Popen(cmd, shell=True)

def stop():
    if triton_process is None or triton_process.poll() is not None:
        return 'Triton not running.'

    triton_process.kill()
    try:
        triton_process.wait(10)
    except subprocess.TimeoutExpired:
        return 'Wait timeout.'

# Create your views here.
class OperationList(APIView):
    serializer_class = OperationSerializer
    
    def get(self, request):
        return Response(OPERATION_CHOICES)
    
    def post(self, request):
        serializer = OperationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'msg': 'Input not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        op = serializer.data['op']
        if op == 'create':
            msg = create()
        elif op == 'remove':
            msg = remove()
        elif op == 'start':
            msg = start()
        elif op == 'stop':
            msg = stop()
        else:
            return Response({'msg': 'Operation not exists.'}, status=status.HTTP_400_BAD_REQUEST)

        if msg is None:
            return Response({'msg': 'Success.'})
        return Response({'msg': msg}, status=status.HTTP_400_BAD_REQUEST)
    