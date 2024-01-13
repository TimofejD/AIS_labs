import datetime

from django.test import TestCase
import random
from .services.repository_service import *

"""
   Данный модуль реализует "тестовые случаи/ситуации" для модуля repository_service.
   Для создания "тестового случая" необходимо создать отдельный класс, который наследует 
   базовый класс TestCase. Класс django.test.TestCase является подклассом unittest.TestCase 
   стандартного Python модуля для тестирования - unittest.

   Более детально см.: https://docs.djangoproject.com/en/4.1/topics/testing/overview/
"""


class TestGreenhouseRepositoryService(TestCase):
    """ Все тестовые методы в классе TestCase (по соглашению)
        должны начинаться с префикса test_* """

    def setUp(self):
        """ Наследуемый метод setUp определяет инструкции,
            которые должны быть выполнены ПЕРЕД тестированием """
        # создаем тестовые записи
        add_plant('Tomato', 25, 50)
        create_greenhouse(gh_name="Greenhouse 1", area_m2=random.uniform(20.0, 29.9), plant=1, tntdata=1)

    def test_get_greenhouse(self):
        """ Тест функции поиска записи Greenhouse по наименованию выращиваемой кульуры """
        plant_in_gh1_rows = get_greenhouse_by_plant_name(plant_name='Tomato')
        for row in plant_in_gh1_rows:
            print(row)
            self.assertIsNotNone(row)  # запись должна существовать
            self.assertTrue(row.Plant_id == 1)  # идентификатор Plant == 1 (т.е. культура Tomato в таблице plant)
            self.assertTrue(row.Plant.name == 'Tomato')  # проверка связи по FK

    def test_delete_greenhouse(self):
        """ Тест функции удаления записи Greenhouse по наименованию выращиваемой культуры """
        delete_greenhouse_by_plant_name(plant_name='Tomato')
        result = get_greenhouse_by_plant_id(plant_id=1)  # ищем запись по идентификатору города Tomato
        self.assertIsNone(result)  # запись не должна существовать

    def tearDown(self):
        """ Наследуемый метод tearDown определяет инструкции,
            которые должны быть выполнены ПОСЛЕ тестирования """
        pass


