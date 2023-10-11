from django.shortcuts import render, redirect
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework import status

from .serializers import GreenhouseSerializer, CultureSerializer
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

    def get(self, request: Request, culture_name: str) -> Response:
        """ Получение всех записей о погоде в населённом пункте """
        response = service.get_all_greehouses_by_culture(culture_name)
        return Response(data=response.data)

    def delete(self, request: Request, culture_name: str) -> Response:
        """ Удаление всех записей о погоде в населённом пункте """
        service.delete_greenhouse_info_by_culture_name(culture_name)
        return Response(status=status.HTTP_200_OK)


class GetPostPutGreenhouse(GenericAPIView):
    serializer_class = GreenhouseSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, *args, **kwargs) -> Response:
        """ Получение записи о погоде в населенном пункте по идентификатору населенного пункта (необходим параметр ?city_id=) """
        culture_id = request.query_params.get('culture_id')        # получаем параметр id из адреса запроса, например: /api/weatherforecast?city_id=1
        if culture_id is None:
            return Response('Expecting query parameter ?culture_id= ', status=status.HTTP_400_BAD_REQUEST)
        response = service.get_greenhouse_by_culture(int(culture_id))
        if response is not None:
            return Response(data=response.data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новую запись о погоде """
        serializer = GreenhouseSerializer(data=request.data)
        if serializer.is_valid():
            service.add_greenhouse_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request: Request, *args, **kwargs) -> Response:
        """ Обновить самую старую запись о погоде """
        serializer = GreenhouseSerializer(data=request.data)
        if serializer.is_valid():
            service.update_greenhouse_info(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class PostCulture(CreateAPIView):
    serializer_class = CultureSerializer
    renderer_classes = [JSONRenderer]

    def post(self, request: Request, *args, **kwargs) -> Response:
        """ Добавить новый населённый пункт """
        serializer = CultureSerializer(data=request.data)
        if serializer.is_valid():
            service.add_culture(serializer)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
