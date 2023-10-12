from ..serializers import GreenhouseSerializer, CultureSerializer
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
                          tntdata=greenhouse_data.get('TnTData_id')
                          )

    def update_greenhouse_info(self, greenhouse: GreenhouseSerializer) -> None:
        greenhouse_data = greenhouse.data
        return update_greenhouse_area_and_culture(gh_name=greenhouse_data.get('GH_Name'),
                                               area_m2=greenhouse_data.get('Area_m2'),
                                               culture_id=greenhouse_data.get('Culture_id'),
                                               )

    def delete_greenhouse_info_by_culture_name(self, culture_name: str) -> None:
        delete_greenhouse_by_culture_name(culture_name.upper())


    def delete_greenhouse_info_by_ghname(self, ghname: str) -> None:
        delete_greenhouse_by_ghname(ghname.upper())

    def add_culture(self, culture: CultureSerializer) -> None:
        culture_data = culture.data
        add_culture(culture_name=culture_data.get('name'),
                    reqtemp=culture_data.get('ReqTempC'),
                    reqhum=culture_data.get('ReqHum')
                    )



