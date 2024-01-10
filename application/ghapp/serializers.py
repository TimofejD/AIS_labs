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


class GreenhouseSerializer(serializers.Serializer):
    GH_Name = serializers.CharField()
    Area_m2 = serializers.IntegerField()
    Culture_id = serializers.IntegerField()
    Schedule_id = serializers.IntegerField()
    SmartModule_id = serializers.IntegerField()
    updated_on = serializers.DateTimeField(required=False)
    """ Класс Serializer позволяет переопределить наследуемые 
        методы create() и update(), в которых, например, можно реализовать бизнес-логику 
        для сохранения или обновления валидируемого объекта (например, для DAO ) """


class CultureSerializer(serializers.Serializer):
    name = serializers.CharField()
    ReqTempC = serializers.FloatField()
    ReqHum = serializers.FloatField()


class ScheduleSerializer(serializers.Serializer):
    Time = serializers.TimeField()
    ReqAction = serializers.CharField()


class SmartModuleSerializer(serializers.Serializer):
    heatModule_id = serializers.IntegerField()
    lightModule_id = serializers.IntegerField()
    ventModule_id = serializers.IntegerField()
    irrigModule_id = serializers.IntegerField()
    curState = serializers.CharField()


class HeatingModuleSerializer(serializers.Serializer):
    mode = serializers.CharField()
    curState = serializers.CharField()


class VentilationModuleSerializer(serializers.Serializer):
    mode = serializers.CharField()
    curState = serializers.CharField()


class LightingModuleSerializer(serializers.Serializer):
    mode = serializers.CharField()
    curState = serializers.CharField()


class IrrigationModuleSerializer(serializers.Serializer):
    mode = serializers.CharField()
    curState = serializers.CharField()

