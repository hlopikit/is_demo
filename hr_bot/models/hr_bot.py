from django.utils import timezone

from hr_bot.models import HrUser, HrChat, HrMessage, HrCheckpoint
from its_utils.app_telegram_bot.models.abstract_bot import AbstractBot

def handle_updates():
    HrBot.objects.get(pk=1).handle_updates()


class HrBot(AbstractBot):
    USER_CLASS = HrUser
    CHAT_CLASS = HrChat
    MESSAGE_CLASS = HrMessage

    """
    Команды 
    start_workday checkpoint stop_workday
    
    Состояния работаю/не работаю
    
    
    
    """

    def on_start_command(self, message, t_user, t_chat, param):
        self.send_message(t_chat.telegram_id, "Команда start принята")

    def on_start_workday_command(self, message, t_user, t_chat, param):
        if not t_user.workday_started:
            t_user.workday_started = timezone.now()
            t_user.workday_chat = t_chat
            t_user.checkpoint = timezone.now()
            t_user.save()
            self.send_message(t_chat.telegram_id,
                              "Рабочий день начат в {}".format(t_user.workday_started))
        else:
            self.send_message(t_chat.telegram_id,
                              "Рабочий день уже начат в {}".format(t_user.workday_started))


    def on_stop_workday_command(self, message, t_user, t_chat, param):
        if t_user.checkpoint and t_user.checkpoint + timezone.timedelta(minutes=3) > timezone.now():
            # Если между чекпоинтом и концом дня прошло всего 3 минуты, то не просим еще раз писать
            t_user.checkpoint = None
            pass

        t_user.workday_started = None
        t_user.save()

        if t_user.checkpoint:
            self.send_message(t_chat.telegram_id, "Напишите про последний интервал")
        else:
            self.on_status_command(message=message, t_user=t_user, t_chat=t_chat, param=param)

    def on_checkpoint_command(self, message, t_user, t_chat, param):
        if not param:
            self.send_message(t_chat.telegram_id, "После команды checkpoint через пробел нужно описать что вы сделали за предыдущий интервал"
                                                  "\n пример:"
                                                  "\n\checkpoint посмотрел видоурок про установку 1С"
                                                  "\nпосмотрел урок про типы переменных"
                                                  "\nустановил и запустил 1с")
            return

        HrCheckpoint.objects.create(
            from_time=t_user.checkpoint or timezone.now(),
            to_time=timezone.now(),
            user=t_user,
            text=param
        )
        if t_user.workday_started:
            t_user.checkpoint = timezone.now()
        else:
            t_user.checkpoint = None
        t_user.save()
        self.send_message(t_chat.telegram_id, "Запись сделана")

    def on_status_command(self, message, t_user, t_chat, param):
        lines = ['Сегодняшний день']
        for cp in HrCheckpoint.objects.filter(to_time__gte=timezone.now().date(), user=t_user):
            lines.append("{:%Y/%m/%d %H:%M:%S}-{:%H:%M:%S} {}".format(timezone.localtime(cp.from_time), timezone.localtime(cp.to_time), cp.text))
        self.send_message(t_chat.telegram_id, "\n".join(lines))