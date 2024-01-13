import datetime
from typing import Optional, Iterable, List
from django.db.models import QuerySet
# Импортируем модели DAO
from ..models import GreenhouseData, Greenhouse, PlantType, Schedule, SmartModule


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

def get_ghdata_by_greenhouse_id(greenhouse_id: int) -> Optional[GreenhouseData]:
    ghdata = GreenhouseData.objects.filter(Greenhouse_id=greenhouse_id).first()
    return ghdata


def get_ghdata_by_greenhouse_name(greenhouse_name: str) -> Optional[GreenhouseData]:
    """ Выборка всех записей о теплице по наименованию выращиваемой культуры """
    ghdata = GreenhouseData.objects.select_related('Greenhouse').filter(Greenhouse__name=greenhouse_name).all()
    return ghdata


def create_ghdata(greenhouse: int, temperature: float, pressure: float) -> None:
    """ Создание нового объекта Greenhouse data  """
    ghdata = GreenhouseData.objects.create(Greenhouse_id=greenhouse, TemperatureC=temperature, CurPressure=pressure)
    ghdata.save()


def update_ghdata_temperature_and_pressure(greenhouse: int, temperature: float, pressure: float) -> None:
    """ Обновление значений площади и названия для теплицы с заданной культурой"""
    ghdata = get_ghdata_by_greenhouse_id(greenhouse)
    ghdata.TemperatureC = temperature
    ghdata.CurPressure = pressure
    ghdata.save()


def delete_ghdata_by_greenhouse_name(gh_name: str) -> None:
    """ Удаление записей о теплице с указанной культурой """
    get_ghdata_by_greenhouse_name(gh_name).delete()


def delete_ghdata_by_greenhouse_id(greenhouse_id: int) -> None:
    """ Удаление записей о теплице с указанной культурой """
    get_ghdata_by_greenhouse_id(greenhouse_id).delete()


def get_greenhouse_by_plant_id(plant_id: int) -> Optional[Greenhouse]:
    """ Выборка одной записи о теплице по идентификатору (PrimaryKey) культуры """
    greenhouse = Greenhouse.objects.filter(Plant_id=plant_id).first()
    return greenhouse


def get_greenhouse_by_plant_name(plant_name: str) -> QuerySet:
    """ Выборка всех записей о теплице по наименованию выращиваемой культуры """
    greenhouse = Greenhouse.objects.select_related('Plant').filter(Plant__name=plant_name).all()
    # объект Greenhouse и связанные объекты Plant (с фильтром по plant_name) будут получены
    # через JOIN-запрос, т.о. при вызове weather.city дополнительных SQL-запросов не будет
    # Конструкция plant__name означает обращение к полю "name" объекта Plant, связанного с Greenhouse через поле "plant"
    return greenhouse


def get_greenhouse_by_ghname(GH_Name: str) -> Optional[Greenhouse]:
    """ Выборка одной записи о теплице по её наименованию """
    greenhouse = Greenhouse.objects.filter(GH_Name=GH_Name).first()
    return greenhouse


def create_greenhouse(gh_name: str, area_m2: float, plant: int, schedule: int, smartmodule: int) -> None:
    """ Создание нового объекта Greenhouse и добавление записей о культуре, расписанию и smart-модулю  """
    greenhouse = Greenhouse.objects.create(GH_Name=gh_name, Area_m2=area_m2, Plant_id=plant,
                                           Schedule_id=schedule, SmartModule_id=smartmodule)
    greenhouse.save()


def update_greenhouse_area_and_plant(gh_name: str, area_m2: float, plant_id: int) -> None:
    """ Обновление значений теплицы"""
    greenhouse = get_greenhouse_by_ghname(gh_name)
    greenhouse.Area_m2 = area_m2
    greenhouse.Plant_id = plant_id
    greenhouse.save()


def delete_greenhouse_by_plant_name(plant_name: str) -> None:
    """ Удаление записей о теплице с указанной культурой """
    get_greenhouse_by_plant_name(plant_name).delete()


def delete_greenhouse_by_ghname(GH_Name: str) -> None:
    """ Удаление записей о теплице с указанной культурой """
    get_greenhouse_by_ghname(GH_Name).delete()


def get_plant_by_name(name: str) -> Optional[PlantType]:
    """ Выборка одной записи о культуре по её идентификатору """
    plant = PlantType.objects.filter(name=name.upper()).first()
    return plant


def add_plant(plant_name: str, reqhum: float) -> None:
    """ Добавление новой выращиваемой культуры """
    plant = PlantType.objects.create(name=plant_name, ReqHum=reqhum)
    plant.save()


def update_plant_temp_and_hum(hum: float, name: str) -> None:
    """ Обновление значений влажности для культуры с заданным id"""
    plant = get_plant_by_name(name)
    plant.ReqHum = hum
    plant.save()


def delete_plant_by_name(name: str) -> None:
    """ Удаление записей о теплице с указанной культурой """
    get_plant_by_name(name).delete()


def get_schedule_by_id(id: int) -> Optional[Schedule]:
    """ Выборка одной записи о расписании по его идентификатору """
    schedule = Schedule.objects.filter(id=id).first()
    return schedule


def add_schedule(begtime: datetime.datetime, endtime: datetime.datetime, periods: datetime.datetime) -> None:
    """ Добавление нового градусника с часами """
    schedule = Schedule.objects.create(BeginTime=begtime, EndTime=endtime, TimePeriods=periods)
    schedule.save()


def update_schedule_periods(id: int, periods: datetime.datetime) -> None:
    """ Обновление значения действия для расписания с заданным id"""
    schedule = get_schedule_by_id(id)
    schedule.TimePeriods = periods
    schedule.save()


def delete_schedule_by_id(id: int) -> None:
    """ Удаление записи о расписании с указанным id """
    get_schedule_by_id(id).delete()


def get_smartmodule_by_id(id: int) -> Optional[SmartModule]:
    """ Выборка одной записи о расписании по его идентификатору """
    smartmodule = SmartModule.objects.filter(id=id).first()
    return smartmodule


def add_smartmodule(heatmod: bool, lightmod: bool, ventmod: bool, irrigmod: bool, state: bool) -> None:
    smartmodule = SmartModule.objects.create(heatModule=heatmod, ventModule=ventmod,
                                             lightModule=lightmod, irrigMod=irrigmod,
                                             curState=state)
    smartmodule.save()


def delete_smartmodule_by_id(id: int) -> None:
    """ Удаление записи о расписании с указанным id """
    get_smartmodule_by_id(id).delete()

