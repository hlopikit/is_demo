from django.conf import settings
from django.db import models




class NumberChoicesType(models.IntegerChoices):
    one = 1, 'Исходящий'
    two = 2, 'Входящий'
    three = 3, 'Входящий с перенаправлением'
    four = 4, 'Обратный'


class NumberChoicesAddToChat(models.IntegerChoices):
    zero = 0, 'Не уведомлять'
    one = 1, 'Уведомлять'


class CallInfo(models.Model):

    user_phone = models.CharField(max_length=20, null=False, blank=False)
    user_id = models.IntegerField(blank=False, null=False)
    phone_number = models.CharField(max_length=50, blank=False, null=False)
    call_date = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField(null=False, blank=False,
                               choices=NumberChoicesType.choices)
    duration = models.IntegerField(null=True, blank=True)
    add_to_chat = models.IntegerField(blank=True, null=True,
                                      choices=NumberChoicesAddToChat.choices)
    call_id = models.CharField(max_length=255, null=True, blank=True)
    record_url = models.FileField(upload_to='rings/', null=True, blank=True)

    def __str__(selfs):
        return (f'Звонок на номер {selfs.phone_number}. '
                f'Время: {selfs.call_date}')

    def telephony_externalcall_register(self, but):
        from mutagen.mp3 import MP3
        res = but.call_api_method("telephony.externalcall.register", {
            "USER_PHONE_INNER": self.user_phone,
            "USER_ID": self.user_id,
            "PHONE_NUMBER": self.phone_number,
            "CALL_START_DATE": self.call_date,
            "TYPE": self.type
        })

        self.call_id = res['result']['CALL_ID']
        self.duration = int(MP3(self.record_url).info.length)
        self.save()

    def telephony_externalcall_finish(self, but):
        but.call_api_method('telephony.externalcall.finish', {
            "CALL_ID": self.call_id,
            "USER_ID": self.user_id,
            "DURATION": self.duration,
            "RECORD_URL": f'{settings.APP_SETTINGS.app_domain}/media/{self.record_url}',
            "ADD_TO_CHAT": self.add_to_chat,
        })

