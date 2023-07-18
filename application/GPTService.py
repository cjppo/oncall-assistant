from application.models import MessagePriority, MessageAssistAdvice, TeamEnum


class GPTService:

    def classify_message(self, message: str):
        return MessageAssistAdvice(MessagePriority.High, TeamEnum.PROMO)
