from dataclasses import dataclass
from enum import IntEnum

from django.db import models


# Create your models here.

@dataclass
class MessageAssistAdvice:
    priority: int
    belongs_to: int


class MessagePriority(IntEnum):
    High = 1,
    Normal = 2,
    Low = 3


class TeamEnum(IntEnum):
    PROMO = 1,
    REWARDS = 2,
    ADSM = 3,
    AFFILIATE = 4,
    UNKNOWN = 5