from django.db.models import *

"""
    В данном модуле реализуются модели Django ORM.
    
    Для управления сущностями БД через веб-интерфейс админиcтратора (django-admin) 
    данные модели должны быть зарегистрированы в модуле admin.py
    
    Подробнее о работе с моделями Django см.: https://docs.djangoproject.com/en/4.1/ref/models/
"""


class Greenhouse(Model):
    id = AutoField(primary_key=True)     # объявление первичного ключа с автоикрементом
    GH_Name = CharField(max_length=100, null=False, unique=True)
    Area_m2 = DecimalField(null=False, max_digits=5, decimal_places=2)    # поле не может быть пустым (NULL)
    Culture = ForeignKey('CultureType', null=False, on_delete=CASCADE)
    Schedule = ForeignKey('Schedule', null=False, on_delete=CASCADE)
    SmartModule = ForeignKey('SmartModule', null=False, on_delete=CASCADE)
    created_on = DateTimeField(auto_now_add=True)   # в поле автоматически генерируется метка времени при создании записи
    updated_on = DateTimeField(auto_now=True)       # в поле автоматически генерируется метка времени при создании записи, метка обновляется при каждой операции UPDATE

    class Meta:
        """ Установка названия таблицы """
        db_table = 'greenhouse'

    def __str__(self):
        """ Метод определяет строковое представление модели """
        return str({'Greenhouse name': self.GH_Name, 'Area_m2': self.Area_m2,
                    'Culture': self.Culture, 'Schedule': self.Schedule, 'SmartModule': self.SmartModule,
                    'created_on': self.created_on, 'updated_on': self.updated_on})


class CultureType(Model):
    """ Тип культуры (название, требуемая влажность и температура) """
    id = AutoField(primary_key=True)
    name = CharField(max_length=100, null=False, unique=True)
    ReqTempC = DecimalField(null=False, max_digits=5, decimal_places=2)
    ReqHum = DecimalField(null=False, max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'culture_type'

    def __str__(self):
        return str({'id': self.id, 'Culture': self.name,
                    'Requested Temperature': self.ReqTempC, 'Requested Humidity': self.ReqHum})


class Schedule(Model):
    """ Таблица с данными с термометра и часов """
    id = AutoField(primary_key=True)
    Time = TimeField(null=False)
    ReqAction = CharField(max_length=100, null=False)

    class Meta:
        db_table = 'schedule'

    def __str__(self):
        return str({'id': self.id, 'Time': self.Time, 'Requested Action': self.ReqAction})


class SmartModule(Model):
    """ Таблица с данными с термометра и часов """
    id = AutoField(primary_key=True)
    heatModule = ForeignKey('HeatingModule', null=False, on_delete=CASCADE)
    ventModule = ForeignKey('VentilationModule', null=False, on_delete=CASCADE)
    lightModule = ForeignKey('LightingModule', null=False, on_delete=CASCADE)
    irrigModule = ForeignKey('IrrigationModule', null=False, on_delete=CASCADE)
    curState = CharField(max_length=100, null=False)

    class Meta:
        db_table = 'Time_schedule'

    def __str__(self):
        return str({'id': self.id, 'Heating Module': self.heatModule, 'Ventilation Module': self.ventModule,
                    'Lighting Module': self.lightModule, 'Irrigation Module': self.irrigModule,
                    'Current State': self.curState})


class HeatingModule(Model):
    """ Таблица с информацией по модулю нагрева"""
    id = AutoField(primary_key=True)
    mode = CharField(max_length=100, null=False)
    curState = CharField(max_length=100, null=False)

    class Meta:
        db_table = 'HeatingModule'

    def __str__(self):
        return str({'id': self.id, 'Heating Mode': self.mode, 'Current State': self.curState})


class VentilationModule(Model):
    """ Таблица с информацией по модулю нагрева"""
    id = AutoField(primary_key=True)
    mode = CharField(max_length=100, null=False)
    curState = CharField(max_length=100, null=False)

    class Meta:
        db_table = 'VentilationModule'

    def __str__(self):
        return str({'id': self.id, 'Ventilation Mode': self.mode, 'Current State': self.curState})


class LightingModule(Model):
    """ Таблица с информацией по модулю нагрева"""
    id = AutoField(primary_key=True)
    mode = CharField(max_length=100, null=False)
    curState = CharField(max_length=100, null=False)

    class Meta:
        db_table = 'LightingModule'

    def __str__(self):
        return str({'id': self.id, 'Lighting Mode': self.mode, 'Current State': self.curState})


class IrrigationModule(Model):
    """ Таблица с информацией по модулю нагрева"""
    id = AutoField(primary_key=True)
    mode = CharField(max_length=100, null=False)
    curState = CharField(max_length=100, null=False)

    class Meta:
        db_table = 'IrrigationModule'

    def __str__(self):
        return str({'id': self.id, 'Lighting Mode': self.mode, 'Current State': self.curState})