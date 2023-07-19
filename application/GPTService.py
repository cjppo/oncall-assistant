from application.models import MessagePriority, MessageAssistAdvice, TeamEnum
import requests
import os
import json

gpt_classify_content = os.environ.get("GPT_CLASSIFY_CONTENT")
gpt_message_check_content = os.environ.get("GPT_MESSAGE_CHECK_CONTENT")
url = 'https://api.openai.com/v1/chat/completions'
headers = {'Accept': '*/*', 'Authorization': 'Bearer ' + os.environ.get('CHAT_GPT_TOKEN')}


def to_team_enum(team):
    if team == "Promotion":
        return TeamEnum.PROMO
    elif team == "Rewards":
        return TeamEnum.REWARDS
    elif team == "affliate":
        return TeamEnum.AFFILIATE
    else:
        return TeamEnum.AFFILIATE


def check_message_if_need_to_deal(message: str):
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": gpt_message_check_content.format(message)
            },
            {
                "role": "user",
                "content": "If someone send such message, do we need handle it: ***{}***, please answer with only one "
                           "word: yes or no".format(message)
            }
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    if response.ok:
        return str(response.json()['choices'][0]['message']['content']).lower().startswith('yes')
    else:
        return False


def classify_message(message: str):
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": gpt_classify_content
            },
            {
                "role": "user",
                "content": "please tell me which project this sentence is most related to: ***{}*** if no project is "
                           "related to sentence, just output: affliate. please answer only one word in the list: ["
                           "Promotion,Rewards,affliate]".format(message)
            }
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    if response.ok:
        return MessageAssistAdvice(MessagePriority.High,
                                   to_team_enum(response.json()['choices'][0]['message']['content']))
    else:
        return MessageAssistAdvice(MessagePriority.Low, TeamEnum.UNKNOWN)
