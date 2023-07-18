from application.models import MessagePriority, MessageAssistAdvice, TeamEnum
import requests
import os


class GPTService:

    def classify_message(self, message: str):
        url = 'https://api.openai.com/v1/chat/completions'
        headers = {'Accept': '*/*', 'Authorization': 'Bearer ' + os.environ.get('CHAT_GPT_TOKEN')}
        json = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": "we have several projects, each projet is responsible for different areas, I will introduce them one by one."
                },
                {
                    "role": "user",
                    "content": "The first project is Promotion. Promotion has a backend service called PromotionV2, and it also has a vendor called talon one. talon one is in charge of maintaining all kinds of campaigns, PromotionV2 acts as a gateway of talon one. promotion now has several types of campaigns. The first type of campaign is general discount campaign, general campaign often assign coupons to target users and users then could redeem the coupon during checkout and then get discount. The second type of campaign is referral campaign, we can also call it out referral program. Referral program is mainly for encourating users to invite friends to afterpay. Advocate could share his referral code to his friend that is not a user of afterpay, his friend then could register afterpay and redeem the referral code, then the friend will get a coupon. The friend could redeem the coupn on his first order, and the advocate could get a reward coupon when the fried make his frist order using afterpay. The third type of campaign is cashback campaign, this campaign acturally serve for cashback service, cashback service is another service inside our system. we can create coupon with safy retry for cashback coupons. The forth type of campaign is vanity campaign, vanity campaign let user to get coupon by themself, our marketers often send a link that has vanity code in the link via email or other channels, target users click the link and could redeem the vanity code and the user could get a coupon, and the coupon could be used in the next order. There are several use cases related to promotion for mobile users. if a consumer has a unused coupon, promotion service will redeem the coupon and give user discounts automatically. there is a page that could show all unused coupons in mobile app, and once user open afterpay mobile app, it will also call promotionV2 to see if there is a available in-store coupon, it will pop up a message if there is a unused in-store coupon. Even if the user has get a coupon, to redeem the coupon and get discount, he also need to meet other requirements, for example, minimum order amount, channels and merchant. Those requirements are set in campaign configuration. Some consumer may call our CS to complain not getting discount, the reason often is that they did not meeting other requirments"
                },
                {
                    "role": "user",
                    "content": "The second project is Rewards. Rewards is a platform that encourage user to use afterpay make more purchase. There are several type of campaigns in rewards, we also call it offer, rewards campaign will give user points and the points could be exchanged to coupon. The firt type of campaign is CLO campaign(offer). the campaign comes from kard or mastercard. kard or mastercard will give money to afterpay, and afterpay will give points to users. The second type of campaign is direct campaign(offer). direct campaigns are created by our marketers, and points will be assigned to users when the order meet requirements, for example, minimum order amount or channel, that depends on the campaign settings. User could gain points by pecentage or a fixed points, that is configured in rewards campaigns. User need to activate the campaign before they can get points. if user does not activate campaign, they will not get points even though they meet other requirements. User get points may not be able to use it right away, the points is pending status, only when they finish payment and the the point could become active, then they could use it. there will be other types of campaigns in future, for example anniversary campaign. user could get points when they join afterpay for 1 year, and the point is active right away in this case."
                },
                {
                    "role": "user",
                    "content": "please tell me which project this sentence is most related to: ***" + message + "***"
                },
                {
                    "role": "user",
                    "content": "if no project is related to sentence, just output: affliate"
                },
                {
                    "role": "user",
                    "content": "please answer only one word in the list: [Promotion,Rewards,affliate]"
                }
            ]
        }
        response = requests.post(url, headers=headers, json = json)
        if response.ok:
            return MessageAssistAdvice(MessagePriority.High, self.toTeamEnume(response.json()['choices'][0]['message']['content']))
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