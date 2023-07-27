from datetime import timedelta

from django.utils import timezone

from hr_bot.models import HrUser, HrChat, HrBot


def cron_notify():
    for t_user in HrUser.objects.exclude(checkpoint=None).filter(checkpoint__lt=timezone.now()-timedelta(hours=1)):
        HrBot.objects.get(pk=1).send_message(t_user.workday_chat.telegram_id, "@{} Пора зачекиниться".format(t_user.username))