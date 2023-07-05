# Пример local_settings
# Измените данные на свои

DEBUG = True
ALLOWED_HOSTS = ['*']

from integration_utils.bitrix24.local_settings_class import LocalSettingsClass

APP_SETTINGS = LocalSettingsClass(
    portal_domain='vladiko.bitrix24.ru',
    app_domain='0.0.0.0:8000',
    app_name='is-demo',
    salt='df897hynadsadasdasdsdaj4b34u804b5n45bkl4b',
    secret_key='sfjbh409890asdasdsaddasd34nk4j4389tfj',
    application_bitrix_client_id='local.5f3e7d07b03783.01669857',
    application_bitrix_client_secret='VjIgCTk8PccYnJ4I25hJb1vdoVfncvQh4gmeZEHXZPE3rm5eGc',
    application_index_path='/',
)



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'is_demo',  # Or path to database file if using sqlite3.
        'USER': 'postgres',  # Not used with sqlite3.
        'PASSWORD': '123456',  # Not used with sqlite3.
        'HOST': 'localhost',
    },
}