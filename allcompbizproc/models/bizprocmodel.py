from django.db import models
from django.db.utils import IntegrityError


class BizprocModel(models.Model):
    process_id = models.IntegerField(unique=True)
    process_name = models.CharField(max_length=200)

    @staticmethod
    def find_all_bizprocs(but):
        res_bizprocs = but.call_list_method('bizproc.workflow.template.list',
                                            {'select': ["ID", "NAME"],
                                             'filter': {"DOCUMENT_TYPE": [
                                                 "crm",
                                                 "CCrmDocumentCompany",
                                                 "COMPANY"
                                             ]}})
        for item in res_bizprocs:
            try:
                bizproc = BizprocModel.objects.create(process_id=item['ID'], process_name=item['NAME'])
                bizproc.save()
            except IntegrityError:
                pass

    def run_cur_bizproc(self, but, company_id):
        but.call_api_method('bizproc.workflow.start', {
            'TEMPLATE_ID': self.process_id,
            'DOCUMENT_ID': ['crm', 'CCrmDocumentCompany', str(company_id)]
        })

    def __str__(self):
        return f"Бизнес процесс {self.process_id} - {self.process_name}"
