from django.db.models import *

"""
    В данном модуле реализуются модели Django ORM.
    
    Для управления сущностями БД через веб-интерфейс админиcтратора (django-admin) 
    данные модели должны быть зарегистрированы в модуле admin.py
    
    Подробнее о работе с моделями Django см.: https://docs.djangoproject.com/en/4.1/ref/models/
"""


class Greenhouse(Model):
    id = AutoField(primary_key=True)     # объявление первичного ключа с автоикрементом
    GH_Name = CharField(max_length=255, null=False, unique=True)
    Area_m2 = DecimalField(null=False, max_digits=5, decimal_places=2)    # поле не может быть пустым (NULL)
    Culture = ForeignKey('CultureType', null=False, on_delete=CASCADE)
    TnTData = ForeignKey('TnTData', null=False, on_delete=CASCADE)
    created_on = DateTimeField(auto_now_add=True)   # в поле автоматически генерируется метка времени при создании записи
    updated_on = DateTimeField(auto_now=True)       # в поле автоматически генерируется метка времени при создании записи, метка обновляется при каждой операции UPDATE

    class Meta:
        """ Установка названия таблицы """
        db_table = 'greenhouse'

    def __str__(self):
        """ Метод определяет строковое представление модели """
        return str({'Greenhouse name': self.GH_Name, 'Area_m2': self.Area_m2,
                    'Culture': self.Culture, 'TnTData': self.TnTData, 'created_on': self.created_on, 'updated_on': self.updated_on})


class CultureType(Model):
    """ Тип культуры (название, требуемая влажность и температура) """
    id = AutoField(primary_key=True)
    name = CharField(max_length=255, null=False, unique=True)
    ReqTempC = DecimalField(null=False, max_digits=5, decimal_places=2)
    ReqHum = DecimalField(null=False, max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'culture_type'

    def __str__(self):
        return str({'id': self.id, 'Culture': self.name})


class TnTData(Model):
    """ Таблица с данными с термометра и часов """
    id = AutoField(primary_key=True)
    Time = TimeField(null=False)
    Temperature_C = DecimalField(null=False, max_digits=5, decimal_places=2)

    class Meta:
        db_table = 'Tnt data'

    def __str__(self):
        return str({'id': self.id, 'Time': self.Time, 'Temp': self.Temperature_C})


class TimeSchedule(Model):
    """ Таблица с данными с термометра и часов """
    id = AutoField(primary_key=True)
    Time = TimeField(null=False)
    ReqAction = CharField(max_length=255, null=False)
    OkAnswer = CharField(max_length=255, default='Not ok')

    class Meta:
        db_table = 'Time_schedule'

    def __str__(self):
        return str({'id': self.id, 'Time': self.Time, 'Required_action': self.ReqAction, 'Ok_answer': self.OkAnswer})
