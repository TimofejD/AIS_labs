import datetime
from typing import Optional, Iterable, List
from django.db.models import QuerySet
# Импортируем модели DAO
from ..models import Greenhouse, CultureType, TnTData, TimeSchedule


"""

    Данный модуль является промежуточным слоем приложения, который отделяет операции 
    для работы с моделями DAO от основной бизнес-логики приложения. Создание данного 
    слоя позволяет унифицировать функции работы с источником данных, и, например, если 
    в приложении нужно будет использовать другой framework для работы с БД, вы можете 
    создать новый модуль (repository_service_newframework.py) и реализовать в нем функции 
    с аналогичными названиями (get_weather_by_city_id, и т.д.). Новый модуль можно будет
    просто импортировать в модуль с основной бизнес-логикой, практически не меняя при этом
    остальной код.
    Также отделение функций работы с БД можно сделать через отдельный абстрактный класс и 
    использовать порождающий паттерн для переключения между необходимыми реализацииями.

"""


def get_greenhouse_by_culture_id(culture_id: int) -> Optional[Greenhouse]:
    """ Выборка одной записи о теплице по идентификатору (PrimaryKey) культуры """
    greenhouse = Greenhouse.objects.filter(Culture_id=culture_id).first()
    # из объекта Weather мы можем получить объекты WeatherType и City через вызов:
    # weather.type
    # weather.city
    # ВАЖНО! Каждый такой вызов будет запускать отдельный SQL-запрос в БД
    return greenhouse


def get_greenhouse_by_culture_name(culture_name: str) -> QuerySet:
    """ Выборка всех записей о теплице по наименованию выращиваемой культуры """
    greenhouse = Greenhouse.objects.select_related('Culture').filter(Culture__name=culture_name).all()
    # объект Weather и связанные объекты City (сфильтром по city_name) будут получены
    # через JOIN-запрос, т.о. при вызове weather.city дополнительных SQL-запросов не будет
    # Конструкция city__name означает обращение к полю "name" объекта City, связанного с Weather через поле "city"
    return greenhouse


def create_greenhouse(gh_name: str, area_m2: float, culture: int, tntdata: int) -> None:
    """ Создание нового объекта Greenhouse и добавление записи о культуре """
    greenhouse = Greenhouse.objects.create(GH_Name=gh_name, Area_m2=area_m2, Culture_id=culture, TnTData_id=tntdata)
    greenhouse.save()


def update_greenhouse_name_and_area(GH_Name: str, Area_m2: float, Сulture: int) -> None:
    """ Обновление значений площади и названия для теплицы с заданной культурой"""
    greenhouse = get_greenhouse_by_culture_id(Сulture)
    greenhouse.GH_Name = GH_Name
    greenhouse.Area_m2 = Area_m2
    greenhouse.save()


def delete_greenhouse_by_culture_name(culture_name: str) -> None:
    """ Удаление записей о теплице с указанной культурой """
    get_greenhouse_by_culture_name(culture_name).delete()


def add_culture(culture_name: str, ReqTemp: float, ReqHum: float) -> None:
    """ Добавление новой выращиваемой культуры """
    culture = CultureType.objects.create(name=culture_name, ReqTempC=ReqTemp, ReqHum=ReqHum)
    culture.save()

def add_tntdata(time: datetime.datetime, temp: float) -> None:
    """ Добавление нового градусника с часами """
    tntdata = TnTData.objects.create(Time=time, Temperature_C=temp)
    tntdata.save()


def add_timeschedule(time: datetime.datetime, action: str, okans: str) -> None:
    timeschedule = TimeSchedule.objects.create(Time=time, ReqAction=action, OkAnswer=okans)
    timeschedule.save()

""" def add_weather_type(weather_type_name: str) -> None: """
""" Добавление нового типа погоды """
"""    weather_type = WeatherType.objects.create(type=weather_type_name)
weather_type.save() """
