from django.db.models import *

"""
    В данном модуле реализуются модели Django ORM.
    
    Для управления сущностями БД через веб-интерфейс админиcтратора (django-admin) 
    данные модели должны быть зарегистрированы в модуле admin.py
    
    Подробнее о работе с моделями Django см.: https://docs.djangoproject.com/en/4.1/ref/models/
"""


class GreenhouseData(Model):
    id = AutoField(primary_key=True)  # объявление первичного ключа с автоикрементом
    Greenhouse = ForeignKey('Greenhouse', null=False, on_delete=CASCADE)
    TemperatureC = DecimalField(null=False, max_digits=5, decimal_places=2)  # поле не может быть пустым (NULL)
    CurPressure = DecimalField(null=False, max_digits=5, decimal_places=2)
    created_on = DateTimeField(auto_now_add=True)  # в поле автоматически генерируется метка времени при создании записи
    
    class Meta:
        """ Установка названия таблицы """
        db_table = 'Greenhouse data'

    def __str__(self):
        """ Метод определяет строковое представление модели """
        return str({'Greenhouse': self.Greenhouse, 'Temperature': self.TemperatureC,
                    'Current Pressure': self.CurPressure, 'created_on': self.created_on})


class Greenhouse(Model):
    id = AutoField(primary_key=True)     # объявление первичного ключа с автоикрементом
    name = CharField(max_length=100, null=False, unique=True)
    Area_m2 = DecimalField(null=False, max_digits=5, decimal_places=2)    # поле не может быть пустым (NULL)
    Plant = ForeignKey('PlantType', null=False, on_delete=CASCADE)
    Schedule = ForeignKey('Schedule', null=False, on_delete=CASCADE)
    SmartModule = ForeignKey('SmartModule', null=False, on_delete=CASCADE)

    class Meta:
        """ Установка названия таблицы """
        db_table = 'Greenhouse'

    def __str__(self):
        """ Метод определяет строковое представление модели """
        return str({'Greenhouse name': self.name, 'Area_m2': self.Area_m2,
                    'Plant': self.Plant, 'Schedule': self.Schedule, 'Smart module': self.SmartModule,})


class PlantType(Model):
    """ Тип культуры (название, требуемая влажность и температура) """
    id = AutoField(primary_key=True)
    name = CharField(max_length=100, null=False, unique=True)
    ReqHum = DecimalField(null=False, max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'Plant type'

    def __str__(self):
        return str({'id': self.id, 'Plant': self.name, 'Requested Humidity': self.ReqHum})


class Schedule(Model):
    """ Таблица расписаний полива"""
    id = AutoField(primary_key=True)
    BeginTime = TimeField(null=False)
    EndTime = TimeField(null=False)
    TimePeriods = TimeField(null=False)

    class Meta:
        db_table = 'Schedule'

    def __str__(self):
        return str({'id': self.id, 'Begin Time': self.BeginTime, 'End Time': self.EndTime,
                    'Watering Frequency': self.TimePeriods})


class SmartModule(Model):
    """ Таблица с данными о смарт-модулях """
    id = AutoField(primary_key=True)
    heatModule = BooleanField(default=True, null=False)
    ventModule = BooleanField(default=True, null=False)
    lightModule = BooleanField(default=True, null=False)
    irrigModule = BooleanField(default=True, null=False)
    curState = BooleanField(default=True)

    class Meta:
        db_table = 'Smart module'

    @property
    def current_state(self):
        return self.irrigModule

    @current_state.setter
    def current_state(self, current_state: bool):
        self.curState = self.heatModule and self.ventModule and self.lightModule and current_state
        self.curState = current_state

    def __str__(self):
        return str({'id': self.id, 'Heating Module': self.heatModule, 'Ventilation Module': self.ventModule,
                    'Lighting Module': self.lightModule, 'Irrigation Module': self.irrigModule,
                    'Current State': self.curState})
