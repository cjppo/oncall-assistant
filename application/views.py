import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
import json
import logging
import os
# Import WebClient from Python SDK (github.com/slackapi/python-slack-sdk)
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from application.GPTService import GPTService
from application.models import MessagePriority, TeamEnum

# WebClient instantiates a client that can call API methods
# When using Bolt, you can use either `app.client` or the `client` passed to listeners.
client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))
logger = logging.getLogger(__name__)
group_id = os.environ.get("SLACK_HACKTHON_GROUP")

# Create your views here.

gptAssistant = GPTService()


@api_view(['GET'])
@csrf_exempt
def healthcheck(request):
    print("called once {}\n".format(time.time() * 1000))
    return HttpResponse(
        "hey",
        content_type="application/json"
    )


def mention_group(ts, belongs_to, channel_id):
    if belongs_to == TeamEnum.PROMO:
        send_slack_message(channel_id, ts, group_id)
    elif belongs_to == TeamEnum.REWARDS:
        send_slack_message(channel_id, ts, group_id)
    elif belongs_to == TeamEnum.ADSM:
        send_slack_message(channel_id, ts, group_id)
    elif belongs_to == TeamEnum.AFFILIATE:
        send_slack_message(channel_id, ts, group_id)
    else:
        send_slack_message(channel_id, ts, group_id)


def send_direct_message(belongs_to):
    if belongs_to == TeamEnum.PROMO:
        send_slack_message(group_id, None, group_id)
    elif belongs_to == TeamEnum.REWARDS:
        send_slack_message(group_id, None, group_id)
    elif belongs_to == TeamEnum.ADSM:
        send_slack_message(group_id, None, group_id)
    elif belongs_to == TeamEnum.AFFILIATE:
        send_slack_message(group_id, None, group_id)
    else:
        send_slack_message(group_id, None, group_id)


def send_slack_message(channel_id, ts, userid):
    try:
        result = client.chat_postMessage(
            channel=channel_id,
            thread_ts=ts,
            text="{}".format(userid)
        )
        print(result)

    except SlackApiError as e:
        print(f"Error: {e}")


@api_view(['POST'])
@csrf_exempt
def webhook(request):
    body = json.loads(request.body)
    channel = body["event"]["channel"]
    if channel == 'C05H9PJRM34' and "parent_user_id" not in body["event"]:
        message = body["event"]["text"]
        print("body: \n {}\n".format(body))
        result = gptAssistant.classify_message(message)
        ts = body["event"]["ts"]
        if (result.priority == MessagePriority.High):
            mention_group(ts, result.belongs_to, 'C05H9PJRM34')
            send_direct_message(result.belongs_to)
        else:
            mention_group(ts, result.belongs_to)
    return HttpResponse(
        "challenge",
        content_type="application/json"
    )
