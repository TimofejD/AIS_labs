from django.shortcuts import render, redirect
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status

from .serializers import GreenhouseSerializer, CultureSerializer, ScheduleSerializer, \
    SmartModuleSerializer, HeatingModuleSerializer, LightingModuleSerializer, \
    VentilationModuleSerializer, IrrigationModuleSerializer
from .services.greenhouse_service import GreenhouseService

"""
    Данный модуль отвечает за обработку соответствующих HTTP операций.
    
    В рамках DRF возможны следующие реализации Django Views 
    (https://www.django-rest-framework.org/tutorial/2-requests-and-responses/):
    
    1. View на основе функций (function based views). Такие функции должны использовать декоратор @api_view.
    2. View на основе классов (class based views). Такие классы должны наследоваться от базовых классов типа APIView 
    (подробнее о class based views см.: https://www.django-rest-framework.org/api-guide/generic-views/).

"""


service = GreenhouseService()      # подключаем слой с бизнес-логикой


class GetDelAllGreenhouse(GenericAPIView):
    serializer_class = GreenhouseSerializer    # определяем сериализатор (необходимо для генерирования страницы Swagger)
    renderer_classes = [JSONRenderer]       # определяем тип входных данных

    def get(self, request: Request, ghname: str) -> Response:
        """ Получение всех записей о теплицах по заданной культуре """
        response = service.get_all_greehouses_by_culture(ghname)
        return Response(data=response.data)

    def delete(self, request: Request, culture_name: str) -> Response:
        """ Удаление всех записей о теплицах по заданной культуре"""
        service.delete_greenhouse_info_by_culture_name(culture_name)
        return Response(status=status.HTTP_200_OK)


class GetPostPutGreenhouse(GenericAPIView):
    serializer_class = GreenhouseSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о теплице по заданной культуре (необходим параметр ?culture_id=) """
        culture_id = request.query_params.get('culture_id')        # получаем параметр id из адреса запроса, например: /api/weatherforecast?city_id=1
        if culture_id is None:
            return Response('Expecting query parameter ?culture_id= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_greenhouse_by_culture(int(culture_id))
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новую запись о теплице """
        serializer = GreenhouseSerializer(data=request.data)
        if serializer.is_valid():
            service.add_greenhouse_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """ Обновить самую старую запись о теплице """
        serializer = GreenhouseSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            service.update_greenhouse_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetPostPutDelCulture(CreateAPIView):
    serializer_class = CultureSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о культуре по заданному названию (необходим параметр ?culture_name=) """
        culture_name = request.query_params.get('culture_name')        # получаем параметр id из адреса запроса, например: /api/weatherforecast?city_id=1
        if culture_name is None:
            return Response('Expecting query parameter ?culture_name= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_culture_by_name(culture_name)
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новую культуру """
        serializer = CultureSerializer(data=request.data)
        if serializer.is_valid():
            service.add_culture(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """ Обновить запись о культуре """
        serializer = CultureSerializer(data=request.data)
        if serializer.is_valid():
            service.update_culture_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, culture_name: str) -> Response:
        """ Удалить запись о кульутре """
        service.delete_culture_info(culture_name)
        return Response(status=status.HTTP_200_OK)


class GetPostPutDelSchedule(CreateAPIView):
    serializer_class = ScheduleSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о расписании по заданному идентефикатору (необходим параметр ?id=) """
        schedule_id = request.query_params.get('id')  # получаем параметр id из адреса запроса, например: /api/weatherforecast?city_id=1
        if schedule_id is None:
            return Response('Expecting query parameter ?id= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_schedule_by_id(schedule_id)
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новое расписание """
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            service.add_schedule(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """ Обновить запись о расписании """
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid():
            service.update_schedule_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, schedule_id: int) -> Response:
        """ Удалить запись о расписании """
        service.delete_schedule_info(schedule_id)
        return Response(status=status.HTTP_200_OK)


class GetPostDelSmartModule(CreateAPIView):
    serializer_class = SmartModuleSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о smart-модуле по заданному идентефикатору (необходим параметр ?id=) """
        module_id = request.query_params.get('id')  # получаем параметр id из адреса запроса, например: /api/weatherforecast?city_id=1
        if module_id is None:
            return Response('Expecting query parameter ?id= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_smartmodule_by_id(module_id)
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новый smart-модуль """
        serializer = SmartModuleSerializer(data=request.data)
        if serializer.is_valid():
            service.add_smartmodule(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, module_id: int) -> Response:
        """ Удалить запись о smart-модуле """
        service.delete_smartmodule_info(module_id)
        return Response(status=status.HTTP_200_OK)


class GetPostDelHeatModule(CreateAPIView):
    serializer_class = HeatingModuleSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о модуле нагрева по заданному идентефикатору (необходим параметр ?id=) """
        module_id = request.query_params.get('id')  # получаем параметр id из адреса запроса, например: /api/weatherforecast?city_id=1
        if module_id is None:
            return Response('Expecting query parameter ?id= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_heatmodule_by_id(module_id)
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новый модуль нагрева """
        serializer = HeatingModuleSerializer(data=request.data)
        if serializer.is_valid():
            service.add_heatmodule(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, module_id: int) -> Response:
        """ Удалить запись о модуле """
        service.delete_heatmodule_info(module_id)
        return Response(status=status.HTTP_200_OK)


class GetPostDelVentModule(CreateAPIView):
    serializer_class = VentilationModuleSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о модуле вентиляции по заданному идентефикатору (необходим параметр ?id=) """
        module_id = request.query_params.get('id')  # получаем параметр id из адреса запроса, например: /api/weatherforecast?city_id=1
        if module_id is None:
            return Response('Expecting query parameter ?id= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_ventmodule_by_id(module_id)
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новый модуль """
        serializer = VentilationModuleSerializer(data=request.data)
        if serializer.is_valid():
            service.add_ventmodule(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, module_id: int) -> Response:
        """ Удалить запись о модуле """
        service.delete_ventmodule_info(module_id)
        return Response(status=status.HTTP_200_OK)


class GetPostDelLightModule(CreateAPIView):
    serializer_class = LightingModuleSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о модуле освещения по заданному идентефикатору (необходим параметр ?id=) """
        module_id = request.query_params.get('id')  # получаем параметр id из адреса запроса, например: /api/weatherforecast?city_id=1
        if module_id is None:
            return Response('Expecting query parameter ?id= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_lightmodule_by_id(module_id)
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новый модуль освещения """
        serializer = LightingModuleSerializer(data=request.data)
        if serializer.is_valid():
            service.add_lightmodule(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, module_id: int) -> Response:
        """ Удалить запись о модуле """
        service.delete_lightmodule_info(module_id)
        return Response(status=status.HTTP_200_OK)


class GetPostDelIrrigationModule(CreateAPIView):
    serializer_class = IrrigationModuleSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о модуле орошения по заданному идентефикатору (необходим параметр ?id=) """
        module_id = request.query_params.get('id')  # получаем параметр id из адреса запроса, например: /api/weatherforecast?city_id=1
        if module_id is None:
            return Response('Expecting query parameter ?id= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_irrigmodule_by_id(module_id)
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новый модуль орошения """
        serializer = IrrigationModuleSerializer(data=request.data)
        if serializer.is_valid():
            service.add_irrigmodule(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, module_id: int) -> Response:
        """ Удалить запись о модуле орошения """
        service.delete_irrigmodule_info(module_id)
        return Response(status=status.HTTP_200_OK)