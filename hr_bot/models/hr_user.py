from datetime import timedelta

from django.db import models
from django.utils import timezone

from hr_bot.models import HrCheckpoint
from its_utils.app_telegram_bot.models.abstract_user import AbstractUser


class HrUser(AbstractUser):
    workday_started = models.DateTimeField(null=True, blank=True)
    checkpoint = models.DateTimeField(null=True, blank=True)
    workday_chat = models.ForeignKey('HrChat', null=True, on_delete=models.PROTECT)

