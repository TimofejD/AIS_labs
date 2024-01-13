from django.apps import AppConfig

"""
    Конфигурационный класс приложения.
    Данный класс должен быть зарегистрирован в setting.py в переменной INSTALLED_APPS 
"""


class GHappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ghapp'
