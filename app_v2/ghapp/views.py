from django.shortcuts import render, redirect
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status

from .serializers import GreenhouseDataSerializer, GreenhouseSerializer, PlantSerializer, ScheduleSerializer, \
    SmartModuleSerializer
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


class GetDelAllGreenhouseData(GenericAPIView):
    serializer_class = GreenhouseDataSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, greenhouse_name: str) -> Response:
        response = service.get_all_ghdata_by_greenhouse_name(greenhouse_name)
        return Response(data=response.data)

    def delete(self, request: Request, greenhouse_name: str) -> Response:
        service.delete_ghdata_info_by_greenhouse_name(greenhouse_name)
        return Response(status=status.HTTP_200_OK)


class GetPostPutGreenhouseData(GenericAPIView):
    serializer_class = GreenhouseDataSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о данных теплице по заданной теплице(необходим параметр ?greenhouse_id=) """
        greenhouse_id = request.query_params.get('greenhouse_id')        # получаем параметр id из адреса запроса, например: /api/weatherforecast?city_id=1
        if greenhouse_id is None:
            return Response('Expecting query parameter ?greenhouse_id= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_ghdata_by_greenhouse(int(greenhouse_id))
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новую запись о теплице """
        serializer = GreenhouseDataSerializer(data=request.data)
        if serializer.is_valid():
            service.add_ghdata_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """ Обновить самую старую запись о теплице """
        serializer = GreenhouseDataSerializer(data=request.data)
        if serializer.is_valid():
            service.update_ghdata_info(serializer)
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetDelAllGreenhouse(GenericAPIView):
    serializer_class = GreenhouseSerializer    # определяем сериализатор (необходимо для генерирования страницы Swagger)
    renderer_classes = [JSONRenderer]       # определяем тип входных данных

    def get(self, request: Request, plant_name: str) -> Response:
        """ Получение всех записей о теплицах по заданной культуре """
        response = service.get_all_greehouses_by_plant(plant_name)
        return Response(data=response.data)

    def delete(self, request: Request, plant_name: str) -> Response:
        """ Удаление всех записей о теплицах по заданной культуре"""
        service.delete_greenhouse_info_by_plant_name(plant_name)
        return Response(status=status.HTTP_200_OK)


class GetPostPutGreenhouse(GenericAPIView):
    serializer_class = GreenhouseSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о теплице по заданной культуре (необходим параметр ?plant_id=) """
        plant_id = request.query_params.get('plant_id')        # получаем параметр id из адреса запроса, например: /api/weatherforecast?city_id=1
        if plant_id is None:
            return Response('Expecting query parameter ?plant_id= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_greenhouse_by_plant(int(plant_id))
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
        if serializer.is_valid():
            service.update_greenhouse_info(serializer)
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetPostPutDelPlant(CreateAPIView):
    serializer_class = PlantSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о культуре по заданному названию (необходим параметр ?plant_name=) """
        plant_name = request.query_params.get('plant_name')        # получаем параметр id из адреса запроса, например: /api/weatherforecast?city_id=1
        if plant_name is None:
            return Response('Expecting query parameter ?plant_name= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_plant_by_name(plant_name)
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новую культуру """
        serializer = PlantSerializer(data=request.data)
        if serializer.is_valid():
            service.add_plant(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """ Обновить запись о культуре """
        serializer = PlantSerializer(data=request.data)
        if serializer.is_valid():
            service.update_plant_info(serializer)
            return Response(status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, plant_name: str) -> Response:
        """ Удалить запись о кульутре """
        service.delete_plant_info(plant_name)
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
            return Response(status=status.HTTP_202_ACCEPTED)
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

