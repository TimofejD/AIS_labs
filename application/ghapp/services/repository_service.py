import datetime
from typing import Optional, Iterable, List
from django.db.models import QuerySet
# Импортируем модели DAO
from ..models import Greenhouse, CultureType, Schedule, SmartModule, HeatingModule, \
    LightingModule, VentilationModule, IrrigationModule


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
    return greenhouse


def get_greenhouse_by_smartmodule_id(smartmodule_id: int) -> Optional[Greenhouse]:
    """ Выборка одной записи о теплице по идентификатору (PrimaryKey) smart модуля """
    greenhouse = Greenhouse.objects.filter(SmartModule_id=smartmodule_id).first()
    return greenhouse


def get_greenhouse_by_culture_name(culture_name: str) -> QuerySet:
    """ Выборка всех записей о теплице по наименованию выращиваемой культуры """
    greenhouse = Greenhouse.objects.select_related('Culture').filter(Culture__name=culture_name).all()
    # объект Greenhouse и связанные объекты Culture (с фильтром по culture_name) будут получены
    # через JOIN-запрос, т.о. при вызове weather.city дополнительных SQL-запросов не будет
    # Конструкция culture__name означает обращение к полю "name" объекта Culture, связанного с Greenhouse через поле "culture"
    return greenhouse


def get_greenhouse_by_ghname(GH_Name: str) -> Optional[Greenhouse]:
    """ Выборка одной записи о теплице по её наименованию """
    greenhouse = Greenhouse.objects.filter(GH_Name=GH_Name).first()
    return greenhouse


def create_greenhouse(gh_name: str, area_m2: float, culture: int, schedule: int, smartmodule: int) -> None:
    """ Создание нового объекта Greenhouse и добавление записей о культуре, расписанию и smart-модулю  """
    greenhouse = Greenhouse.objects.create(GH_Name=gh_name, Area_m2=area_m2, Culture_id=culture,
                                           Schedule_id=schedule, SmartModule_id=smartmodule)
    greenhouse.save()


def update_greenhouse_area_and_culture(gh_name: str, area_m2: float, culture_id: int) -> None:
    """ Обновление значений площади и названия для теплицы с заданной культурой"""
    greenhouse = get_greenhouse_by_ghname(gh_name)
    greenhouse.Area_m2 = area_m2
    greenhouse.Culture_id = culture_id
    greenhouse.save()


def delete_greenhouse_by_culture_name(culture_name: str) -> None:
    """ Удаление записей о теплице с указанной культурой """
    get_greenhouse_by_culture_name(culture_name).delete()


def delete_greenhouse_by_ghname(GH_Name: str) -> None:
    """ Удаление записей о теплице с указанной культурой """
    get_greenhouse_by_ghname(GH_Name).delete()

def get_culture_by_name(name: str) -> Optional[CultureType]:
    """ Выборка одной записи о культуре по её идентификатору """
    culture = CultureType.objects.filter(name=name.upper()).first()
    return culture

def add_culture(culture_name: str, reqtemp: float, reqhum: float) -> None:
    """ Добавление новой выращиваемой культуры """
    culture = CultureType.objects.create(name=culture_name, ReqTempC=reqtemp, ReqHum=reqhum)
    culture.save()

def update_culture_temp_and_hum(temp: float, hum: float, name: str) -> None:
    """ Обновление значений температуры и влажности для культуры с заданным id"""
    culture = get_culture_by_name(name)
    culture.ReqTempC = temp
    culture.ReqHum = hum
    culture.save()

def delete_culture_by_name(name: str) -> None:
    """ Удаление записей о теплице с указанной культурой """
    get_culture_by_name(name).delete()

def get_schedule_by_id(id: int) -> Optional[Schedule]:
    """ Выборка одной записи о расписании по его идентификатору """
    schedule = Schedule.objects.filter(id=id).first()
    return schedule

def add_schedule(time: datetime.datetime, reqaction: str) -> None:
    """ Добавление нового градусника с часами """
    schedule = Schedule.objects.create(Time=time, ReqAction=reqaction)
    schedule.save()

def update_schedule_action(id: int, action: str) -> None:
    """ Обновление значения действия для расписания с заданным id"""
    schedule = get_schedule_by_id(id)
    schedule.ReqAction = action
    schedule.save()

def delete_schedule_by_id(id: int) -> None:
    """ Удаление записи о расписании с указанным id """
    get_schedule_by_id(id).delete()

def get_smartmodule_by_id(id: int) -> Optional[SmartModule]:
    """ Выборка одной записи о расписании по его идентификатору """
    smartmodule = SmartModule.objects.filter(id=id).first()
    return smartmodule

def add_smartmodule(heatmod: int, lightmod: int, ventmod: int, irrigmod: int, state: str) -> None:
    smartmodule = SmartModule.objects.create(heatModule=heatmod, ventModule=ventmod,
                                             lightModule=lightmod, irrigMod=irrigmod,
                                             curState=state)
    smartmodule.save()

def delete_smartmodule_by_id(id: int) -> None:
    """ Удаление записи о расписании с указанным id """
    get_smartmodule_by_id(id).delete()

def get_heatmodule_by_id(id: int) -> Optional[HeatingModule]:
    """ Выборка одной записи о расписании по его идентификатору """
    heatmodule = HeatingModule.objects.filter(id=id).first()
    return heatmodule

def add_heatmodule(mode: str, state: str) -> None:
    heatmodule = HeatingModule.objects.create(mode=mode, curState=state)
    heatmodule.save()

def delete_heatmodule_by_id(id: int) -> None:
    """ Удаление записи о расписании с указанным id """
    get_heatmodule_by_id(id).delete()

def get_ventmodule_by_id(id: int) -> Optional[VentilationModule]:
    """ Выборка одной записи о расписании по его идентификатору """
    ventmodule = VentilationModule.objects.filter(id=id).first()
    return ventmodule

def add_ventmodule(mode: str, state: str) -> None:
    ventmodule = VentilationModule.objects.create(mode=mode, curState=state)
    ventmodule.save()

def delete_ventmodule_by_id(id: int) -> None:
    """ Удаление записи о расписании с указанным id """
    get_ventmodule_by_id(id).delete()

def get_lightmodule_by_id(id: int) -> Optional[LightingModule]:
    """ Выборка одной записи о расписании по его идентификатору """
    module = LightingModule.objects.filter(id=id).first()
    return module

def add_lightmodule(mode: str, state: str) -> None:
    module = LightingModule.objects.create(mode=mode, curState=state)
    module.save()

def delete_lightmodule_by_id(id: int) -> None:
    """ Удаление записи о расписании с указанным id """
    get_lightmodule_by_id(id).delete()

def get_irrigmodule_by_id(id: int) -> Optional[IrrigationModule]:
    """ Выборка одной записи о расписании по его идентификатору """
    module = IrrigationModule.objects.filter(id=id).first()
    return module

def add_irrigmodule(mode: str, state: str) -> None:
    module = IrrigationModule.objects.create(mode=mode, curState=state)
    module.save()

def delete_irrigmodule_by_id(id: int) -> None:
    """ Удаление записи о расписании с указанным id """
    get_irrigmodule_by_id(id).delete()

