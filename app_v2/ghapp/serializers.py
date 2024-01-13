from rest_framework import serializers


"""
    В данном модуле реализуются сериализаторы DRF, позволяющие 
    валидировать данные для моделей DAO (models.py), 
    а также сериализующие (преобразующие) эти модели в стандартные 
    объекты Python (dict) и в формат json. Подробнее см.: 
    https://www.django-rest-framework.org/api-guide/serializers/
    https://www.django-rest-framework.org/api-guide/fields/
    
    Сериализаторы DRF являются аналогом DTO для Django. 
"""


class GreenhouseDataSerializer(serializers.Serializer):
    Greenhouse_id = serializers.IntegerField()
    TemperatureC = serializers.FloatField()
    CurPressure = serializers.FloatField()


class GreenhouseSerializer(serializers.Serializer):
    name = serializers.CharField()
    Area_m2 = serializers.IntegerField()
    Plant_id = serializers.IntegerField()
    Schedule_id = serializers.IntegerField()
    SmartModule_id = serializers.IntegerField()
    """ Класс Serializer позволяет переопределить наследуемые 
        методы create() и update(), в которых, например, можно реализовать бизнес-логику 
        для сохранения или обновления валидируемого объекта (например, для DAO ) """


class PlantSerializer(serializers.Serializer):
    name = serializers.CharField()
    ReqHum = serializers.FloatField()


class ScheduleSerializer(serializers.Serializer):
    BeginTime = serializers.TimeField()
    EndTime = serializers.TimeField()
    TimePeriods = serializers.TimeField()


class SmartModuleSerializer(serializers.Serializer):
    heatModule = serializers.BooleanField()
    lightModule = serializers.BooleanField()
    ventModule = serializers.BooleanField()
    irrigModule = serializers.BooleanField()
    curState = serializers.BooleanField()

