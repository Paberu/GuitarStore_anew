from django.test import TestCase

from shop.models import Manufacturer


class TestModel(TestCase):

    @classmethod
    def setUpTestData(cls):
        manufacturer = Manufacturer.objects.create()

    def setUp(self) -> None:
        print('setUp вызывается перед каждым тестом')

    def tearDown(self) -> None:
        print('tearDown вызывается после каждого теста')