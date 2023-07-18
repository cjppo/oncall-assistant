from application.models import MessagePriority, MessageAssistAdvice, TeamEnum


class GPTService:

    def classify_message(message):
        return MessageAssistAdvice(MessagePriority.High, TeamEnum.PROMO)
