import base64
import json
import os
import time
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET'])
@csrf_exempt
def healthcheck(request):
    print("called once {}\n".format(time.time()*1000))
    return HttpResponse(
        "hey",
        content_type="application/json"
    )