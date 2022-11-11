from django.test import TestCase

from shop.forms import SearchForm, OrderModelForm


class SearchFormTest(TestCase):

    def test_q_placeholder(self):
        form = SearchForm()
        self.assertEqual(form.fields['query'].widget.attrs['placeholder'], 'Поиск')


class OrderFormTest(TestCase):

    def test_delivery_choices(self):
        DELIVERY_CHOICES = [
            (0, 'Выберите, пожалуйста'),
            (1, 'Доставка'),
            (2, 'Самовывоз'),
        ]
        form = OrderModelForm()
        self.assertEqual(form.fields['delivery'].choices, DELIVERY_CHOICES)

    def test_delivery_label(self):
        form = OrderModelForm()
        self.assertEqual(form.fields['delivery'].label, 'Доставка')

    def test_delivery_coerce(self):
        form = OrderModelForm()
        self.assertEqual(form.fields['delivery'].coerce, int)

    def test_delivery_1(self):
        data = {'customer': 'Имя', 'email':'abc@abc.ru', 'phone':'183679238', 'address':'', 'delivery': 2}
        form = OrderModelForm(data=data)
        self.assertTrue(form.is_valid())

    def test_delivery_2(self):
        data = {'customer': 'Имя', 'email':'abc@abc.ru', 'phone':'183679238', 'address':'', 'delivery': 1}
        form = OrderModelForm(data=data)
        self.assertFalse(form.is_valid())