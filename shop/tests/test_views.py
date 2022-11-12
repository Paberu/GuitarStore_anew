from django.test import TestCase

from shop.models import Section


class OrderViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        section = Section()