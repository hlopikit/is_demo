import os
import settings

from django.http import FileResponse
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from .utils import save_file


@main_auth(on_cookies=True)
def product_in_excel(request):

    but = request.bitrix_user_token
    if request.method == 'POST':
        products = but.call_list_method('crm.product.list')
        users = but.call_list_method('user.get')

        save_file(products, users)
        file_path = os.path.join(settings.BASE_DIR, 'example.xlsx')
        # Открываем файл для чтения
        file = open(file_path, 'rb')
        # Создаем объект FileResponse для файла
        response = FileResponse(file)
        # Устанавливаем заголовок Content-Disposition для указания имени файла
        response['Content-Disposition'] = 'attachment; filename="example.xlsx"'

        # Возвращаем объект FileResponse в качестве ответа HTTP
        return response

    return render(request, 'productexcellist.html', locals())
