from django.contrib import admin
from .models import *

"""
    В данном модуле регистрируются модели Django 
    для доступа через веб-интерфейс админиcтратора (django-admin)
"""

admin.site.register(Greenhouse)
admin.site.register(CultureType)
admin.site.register(TnTData)
admin.site.register(TimeSchedule)
