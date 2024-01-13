from ..serializers import (GreenhouseDataSerializer, GreenhouseSerializer, PlantSerializer, ScheduleSerializer,
                           SmartModuleSerializer)
from .repository_service import *


"""

    Данный модуль содержит программный слой с реализацией дополнительной бизнес-логики, 
    выполняемой перед или после выполнения операций над хранилищем данных (repository), 
    а также выполнение дополнительных операций над сериализаторами (если необходимо).

    ВАЖНО! Реализация данного слоя приведена в качестве демонстрации полной структуры RESTful веб-сервиса.
           В небольших проектах данный слой может быть избыточен, в таком случае, из контроллера ваших маршрутов 
           (Router в FastAPI или View в Django) можно напрямую работать с функциями хранилища данных (repository_service).
"""


class GreenhouseService:
    def get_ghdata_by_greenhouse(self, greenhouse_id: int) -> Optional[GreenhouseDataSerializer]:
        result = get_ghdata_by_greenhouse_id(greenhouse_id)
        if result is not None:
            return GreenhouseDataSerializer(result)
        return result

    def get_all_ghdata_by_greenhouse_name(self, greenhouse_name: str) -> GreenhouseDataSerializer:
        result = get_ghdata_by_greenhouse_name(greenhouse_name)
        ghdata = GreenhouseDataSerializer(result, many=True)
        return ghdata


    def add_ghdata_info(self, ghdata: GreenhouseDataSerializer) -> None:
        greenhouse_data = ghdata.data     # получаем валидированные с помощью сериализатора данные (метод .data  возвращает объект типа dict)
        create_ghdata(greenhouse=greenhouse_data.get('Greenhouse_id'),
                      temperature=greenhouse_data.get('TemperatureC'),
                      pressure=greenhouse_data.get('CurPressure')
                      )

    def update_ghdata_info(self, ghdata: GreenhouseDataSerializer) -> None:
        greenhouse_data = ghdata.data
        return update_ghdata_temperature_and_pressure(greenhouse=greenhouse_data.get('Greenhouse_id'),
                                                      temperature=greenhouse_data.get('TemperatureC'),
                                                      pressure=greenhouse_data.get('CurPressure')
                                                      )

    def delete_ghdata_info_by_greenhouse_name(self, gh_name: str) -> None:
        delete_ghdata_by_greenhouse_name(gh_name.upper())

    def delete_greenhouse_info_by_greenhouse_id(self, gh_id: int) -> None:
        delete_ghdata_by_greenhouse_id(gh_id)

    def get_greenhouse_by_plant(self, plant_id: int) -> Optional[GreenhouseSerializer]:
        result = get_greenhouse_by_plant_id(plant_id)
        if result is not None:
            return GreenhouseSerializer(result)
        return result

    def get_all_greehouses_by_plant(self, plant_name: str) -> GreenhouseSerializer:
        result = get_greenhouse_by_plant_name(plant_name)
        greenhouse_data = GreenhouseSerializer(result, many=True)     # для возвращения списка объектов, необходимо создание сериализатора с аргументом many=True
        return greenhouse_data

    def add_greenhouse_info(self, greenhouse: GreenhouseSerializer) -> None:
        greenhouse_data = greenhouse.data     # получаем валидированные с помощью сериализатора данные (метод .data  возвращает объект типа dict)
        create_greenhouse(gh_name=greenhouse_data.get('GH_Name'),
                          area_m2=greenhouse_data.get('Area_m2'),
                          plant=greenhouse_data.get('Plant_id'),
                          schedule=greenhouse_data.get('Schedule_id'),
                          smartmodule=greenhouse_data.get('SmartModule_id')
                          )

    def update_greenhouse_info(self, greenhouse: GreenhouseSerializer) -> None:
        greenhouse_data = greenhouse.data
        return update_greenhouse_area_and_plant(gh_name=greenhouse_data.get('GH_Name'),
                                                area_m2=greenhouse_data.get('Area_m2'),
                                                plant_id=greenhouse_data.get('Plant_id')
                                                )

    def delete_greenhouse_info_by_plant_name(self, plant_name: str) -> None:
        delete_greenhouse_by_plant_name(plant_name.upper())


    def delete_greenhouse_info_by_ghname(self, ghname: str) -> None:
        delete_greenhouse_by_ghname(ghname.upper())

    def get_plant_by_name(self, name: str) -> Optional[PlantSerializer]:
        result = get_plant_by_name(name)
        if result is not None:
            return PlantSerializer(result)
        return result

    def add_plant(self, plant: PlantSerializer) -> None:
        plant_data = plant.data
        add_plant(plant_name=plant_data.get('name'),
                  reqhum=plant_data.get('ReqHum')
                  )

    def update_plant_info(self, plant: PlantSerializer) -> None:
        plant_data = plant.data
        update_plant_temp_and_hum(hum=plant_data.get('ReqHum'),
                                  name=plant_data.get('name')
                                  )

    def delete_plant_info(self, name: str) -> None:
        delete_plant_by_name(name.upper())

    def get_schedule_by_id(self, sc_id: int) -> Optional[ScheduleSerializer]:
        result = get_schedule_by_id(sc_id)
        if result is not None:
            return ScheduleSerializer(result)
        return result

    def add_schedule(self, schedule: ScheduleSerializer) -> None:
        schedule_data = schedule.data
        add_schedule(begtime=schedule_data.get('BeginTime'),
                     endtime=schedule_data.get('EndTime'),
                     periods=schedule_data.get('TimePeriods')
                     )

    def update_schedule_info(self, schedule: ScheduleSerializer) -> None:
        schedule_data = schedule.data
        update_schedule_periods(id=schedule_data.get('id'),
                                periods=schedule_data.get('TimePeriods')
                                )

    def delete_schedule_info(self, id: int) -> None:
        delete_schedule_by_id(id)

    def get_smartmodule_by_id(self, sm_id: int) -> Optional[SmartModuleSerializer]:
        result = get_smartmodule_by_id(sm_id)
        if result is not None:
            return SmartModuleSerializer(result)
        return result

    def add_smartmodule(self, smartmodule: SmartModuleSerializer) -> None:
        smartmodule_data = smartmodule.data
        add_smartmodule(heatmod=smartmodule_data.get('heatModule'),
                        lightmod=smartmodule_data.get('lightModule'),
                        ventmod=smartmodule_data.get('ventModule'),
                        irrigmod=smartmodule_data.get('irrigModule'),
                        state=smartmodule_data.get('curState')
                        )

    def delete_smartmodule_info(self, id: int) -> None:
        delete_smartmodule_by_id(id)

