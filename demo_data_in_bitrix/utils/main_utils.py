import os.path
import time
from functools import cached_property

import requests

from callsuploader.models.models import CallInfo
from django.conf import settings


import pandas as pd

from .secondary_utils import *

OBJECT_CRM = {"Лиды": 1,
              "Сделки": 2,
              "Контакты": 3,
              "Компании": 4,
              "Коммерческие предложения": 7,
              "Новые счета": 31}


class DataImporter:

    def __init__(self, filename, but):
        self.but = but
        self.excel_file = pd.ExcelFile(filename)
        self.object_count = dict()
        self.companies_origin_id_dict = None

    def __call__(self, methods):
        for method in methods:
            try:
                method(self)
            except ValueError:
                pass

    @cached_property
    def _load_origin_id_prefix(self):
        return time.time()

    # Загружаем компании
    def load_companies(self):
        company_data = self.excel_file.parse('Компании').to_dict("records")
        company_data = add_origin_prefix(company_data, self._load_origin_id_prefix)
        self.object_count.update({"Компании": len(company_data)})
        load_crm(company_data, self.but, "4")

        companies = self.but.call_list_method('crm.company.list', {
            "SELECT": ["ORIGIN_ID", "ID"],
            "FILTER": {"%ORIGIN_ID": "{}_".format(self._load_origin_id_prefix)}})
        # Используем прием конвертации в адресный dict https://it-solution.kdb24.ru/article/218199/
        # после этого легко найдем companies_origin_id_dict['1690182208.5614886_7']['ID']
        self.companies_origin_id_dict = {item['ORIGIN_ID']: item for item in companies}
        for d in company_data:
            # https://dev.1c-bitrix.ru/rest_help/crm/requisite/methods/crm_address_add.php
            self.but.call_api_method("crm.address.add", {"fields": {
                "TYPE_ID": "1",  # Фактический адрес?
                "ENTITY_TYPE_ID": "4",  # 4 - для Компаний
                "ENTITY_ID": self.companies_origin_id_dict[d['ORIGIN_ID']]['ID'],
                "CITY": d["ADDRESS_CITY"],
                "ADDRESS_1": d["ADDRESS"],
            }})

    # Загружаем контакты
    def load_contacts(self):
        contacts_data = self.excel_file.parse('Контакты').to_dict("records")
        contacts_data = add_origin_prefix(contacts_data, self._load_origin_id_prefix)
        # Можно же грузить контакты без компаний
        if self.companies_origin_id_dict is not None:
            contacts_data = make_links_from_origin(contacts_data,
                                                   'COMPANY_ORIGIN_ID',
                                                   'COMPANY_ID',
                                                   self.companies_origin_id_dict,
                                                   self._load_origin_id_prefix)
        for c in contacts_data:
            c["PHONE"] = [{"VALUE": str(c["PHONE"]), "VALUE_TYPE": "WORK"}]

        self.object_count["Контакты"] = len(contacts_data)
        load_crm(contacts_data, self.but, "3")

    # Загружаем сделки
    def load_deals(self):
        deals_data = self.excel_file.parse('Сделки').to_dict("records")
        self.object_count["Сделки"] = len(deals_data)
        load_crm(deals_data, self.but, "2")

    # Загружаем лиды
    def load_leads(self):
        leads_data = self.excel_file.parse('Лиды').to_dict("records")
        self.object_count["Лиды"] = len(leads_data)
        load_crm(leads_data, self.but, "1")

    # Загружаем звонки
    def load_calls(self):
        calls_data = self.excel_file.parse('Звонки').to_dict('records')
        self.object_count["Звонки"] = len(calls_data)
        for c in calls_data:
            call = CallInfo(
                user_phone=c["user_phone"],
                user_id=int(c["user_id"]),
                phone_number=c["phone_number"],
                call_date=c["call_date"],
                type=int(c["type"]),
                add_to_chat=int(c["add_to_chat"])
            )
            call.save()

            drive_id = c["file"].split("/")[-2]
            url = "https://drive.google.com/uc?id=" + drive_id + "&export=download"
            r = requests.get(url, allow_redirects=True)

            file_path = os.path.join(call.inner_media_path, str(call.id) + '.mp3')
            with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb') as file:
                file.write(r.content)

            call.file.name = file_path
            call.save()

            call.telephony_externalcall_register(self.but)
            call.telephony_externalcall_finish(self.but)
            call.wav_maker_n_messages(self.but)
            os.remove(file_path)


