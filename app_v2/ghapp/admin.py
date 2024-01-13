from django.contrib import admin
from .models import *

"""
    В данном модуле регистрируются модели Django 
    для доступа через веб-интерфейс админиcтратора (django-admin)
"""

admin.site.register(GreenhouseData)
admin.site.register(Greenhouse)
admin.site.register(PlantType)
admin.site.register(Schedule)
admin.site.register(SmartModule)
