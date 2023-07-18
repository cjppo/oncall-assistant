from application.models import MessagePriority, MessageAssistAdvice, TeamEnum
import requests
import os
import json

gpt_classify_content = os.environ.get("GPT_CLASSIFY_CONTENT")


class GPTService:

    def classify_message(self, message: str):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {'Accept': '*/*', 'Authorization': 'Bearer ' + os.environ.get('CHAT_GPT_TOKEN')}
        json = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": gpt_classify_content.format(message)
                }
            ]
        }
        response = requests.post(url, headers=headers, json=json)
        if response.ok:
            return MessageAssistAdvice(MessagePriority.High,
                                       self.toTeamEnume(response.json()['choices'][0]['message']['content']))
        else:
            return MessageAssistAdvice(MessagePriority.Low, TeamEnum.UNKNOWN)

    def toTeamEnume(self, team):
        if team == "Promotion":
            return TeamEnum.PROMO
        elif team == "Rewards":
            return TeamEnum.REWARDS
        elif team == "affliate":
            return TeamEnum.AFFILIATE
        else:
            return TeamEnum.UNKNOWN
