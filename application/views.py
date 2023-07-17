import base64
import json
import os
import time
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json

# Create your views here.

@api_view(['GET'])
@csrf_exempt
def healthcheck(request):
    print("called once {}\n".format(time.time()*1000))
    return HttpResponse(
        "hey",
        content_type="application/json"
    )

@api_view(['POST'])
@csrf_exempt
def webhook(request):
    body = json.loads(request.body)
    channel = body["event"]["channel"]
    if channel == 'C05H9PJRM34' and "parent_user_id" not in body["event"]:
        message = json.loads(request.body)["event"]["text"]
        print("body: \n {}\n".format(body))
    return HttpResponse(
        "challenge",
        content_type="application/json"
    )