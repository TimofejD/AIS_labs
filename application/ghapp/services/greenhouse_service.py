from ..serializers import GreenhouseSerializer, CultureSerializer, ScheduleSerializer, SmartModuleSerializer, \
    HeatingModuleSerializer, LightingModuleSerializer, VentilationModuleSerializer, IrrigationModuleSerializer
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

    def get_greenhouse_by_culture(self, culture_id: int) -> Optional[GreenhouseSerializer]:
        result = get_greenhouse_by_culture_id(culture_id)
        if result is not None:
            return GreenhouseSerializer(result)
        return result

    def get_all_greehouses_by_culture(self, culture_name: str) -> GreenhouseSerializer:
        result = get_greenhouse_by_culture_name(culture_name.upper())
        greenhouse_data = GreenhouseSerializer(result, many=True)     # для возвращения списка объектов, необходимо создание сериализатора с аргументом many=True
        return greenhouse_data

    def add_greenhouse_info(self, greenhouse: GreenhouseSerializer) -> None:
        greenhouse_data = greenhouse.data     # получаем валидированные с помощью сериализатора данные (метод .data  возвращает объект типа dict)
        create_greenhouse(gh_name=greenhouse_data.get('GH_Name'),
                          area_m2=greenhouse_data.get('Area_m2'),
                          culture=greenhouse_data.get('Culture_id'),
                          schedule=greenhouse_data.get('Schedule_id'),
                          smartmodule=greenhouse_data.get('SmartModule_id')
                          )

    def update_greenhouse_info(self, greenhouse: GreenhouseSerializer) -> None:
        greenhouse_data = greenhouse.data
        return update_greenhouse_area_and_culture(gh_name=greenhouse_data.get('GH_Name'),
                                                  area_m2=greenhouse_data.get('Area_m2'),
                                                  culture_id=greenhouse_data.get('Culture_id')
                                                  )

    def delete_greenhouse_info_by_culture_name(self, culture_name: str) -> None:
        delete_greenhouse_by_culture_name(culture_name.upper())


    def delete_greenhouse_info_by_ghname(self, ghname: str) -> None:
        delete_greenhouse_by_ghname(ghname.upper())

    def get_culture_by_name(self, name: str) -> Optional[CultureSerializer]:
        result = get_culture_by_name(name)
        if result is not None:
            return CultureSerializer(result)
        return result

    def add_culture(self, culture: CultureSerializer) -> None:
        culture_data = culture.data
        add_culture(culture_name=culture_data.get('name'),
                    reqtemp=culture_data.get('ReqTempC'),
                    reqhum=culture_data.get('ReqHum')
                    )

    def update_culture_info(self, culture: CultureSerializer) -> None:
        culture_data = culture.data
        update_culture_temp_and_hum(temp=culture_data.get('ReqTempC'),
                                    hum=culture_data.get('ReqHum'),
                                    name=culture_data.get('name')
                                    )

    def delete_culture_info(self, name: str) -> None:
        delete_culture_by_name(name.upper())

    def get_schedule_by_id(self, sc_id: int) -> Optional[ScheduleSerializer]:
        result = get_schedule_by_id(sc_id)
        if result is not None:
            return ScheduleSerializer(result)
        return result

    def add_schedule(self, schedule: ScheduleSerializer) -> None:
        schedule_data = schedule.data
        add_schedule(time=schedule_data.get('Time'),
                     reqaction=schedule_data.get('ReqAction')
                     )

    def update_schedule_info(self, schedule: ScheduleSerializer) -> None:
        schedule_data = schedule.data
        update_schedule_action(action=schedule_data.get('ReqAction'),
                               id=schedule_data.get('id')
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

    def get_heatmodule_by_id(self, hm_id: int) -> Optional[HeatingModuleSerializer]:
        result = get_heatmodule_by_id(hm_id)
        if result is not None:
            return HeatingModuleSerializer(result)
        return result

    def add_heatmodule(self, heatmodule: HeatingModuleSerializer) -> None:
        heatmodule_data = heatmodule.data
        add_heatmodule(mode=heatmodule_data.get('mode'),
                       state=heatmodule_data.get('curState')
                       )

    def delete_heatmodule_info(self, id: int) -> None:
        delete_heatmodule_by_id(id)

    def get_ventmodule_by_id(self, vm_id: int) -> Optional[VentilationModuleSerializer]:
        result = get_ventmodule_by_id(vm_id)
        if result is not None:
            return VentilationModuleSerializer(result)
        return result

    def add_ventmodule(self, ventmodule: VentilationModuleSerializer) -> None:
        ventmodule_data = ventmodule.data
        add_ventmodule(mode=ventmodule_data.get('mode'),
                       state=ventmodule_data.get('curState')
                       )

    def delete_ventmodule_info(self, id: int) -> None:
        delete_ventmodule_by_id(id)

    def get_lightmodule_by_id(self, lm_id: int) -> Optional[LightingModuleSerializer]:
        result = get_lightmodule_by_id(lm_id)
        if result is not None:
            return LightingModuleSerializer(result)
        return result

    def add_lightmodule(self, lightmodule: LightingModuleSerializer) -> None:
        lightmodule_data = lightmodule.data
        add_lightmodule(mode=lightmodule_data.get('mode'),
                        state=lightmodule_data.get('curState')
                        )

    def delete_lightmodule_info(self, id: int) -> None:
        delete_lightmodule_by_id(id)

    def get_irrigmodule_by_id(self, im_id: int) -> Optional[IrrigationModuleSerializer]:
        result = get_irrigmodule_by_id(im_id)
        if result is not None:
            return IrrigationModuleSerializer(result)
        return result

    def add_irrigmodule(self, irrigmodule: IrrigationModuleSerializer) -> None:
        irrigmodule_data = irrigmodule.data
        add_irrigmodule(mode=irrigmodule_data.get('mode'),
                        state=irrigmodule_data.get('curState')
                        )

    def delete_irrigmodule_info(self, id: int) -> None:
        delete_irrigmodule_by_id(id)