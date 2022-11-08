from django import forms
from django.core.exceptions import ValidationError

from shop.models import Order


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Поиск'}))


class OrderModelForm(forms.ModelForm):

    DELIVERY_CHOICES = (
        (0, 'Выберите, пожалуйста'),
        (1, 'Доставка'),
        (2, 'Самовывоз'),
    )
    delivery = forms.TypedChoiceField(label='Доставка', choices=DELIVERY_CHOICES, coerce=int)

    class Meta:
        model = Order
        exclude = ['needs_delivery', 'discount', 'status']
        labels = {
            'address': 'Полный адрес доставки, шурум-бурум',
            'notice': 'Примечание к заказу'
        }
        widgets = {
            'address': forms.Textarea(
                attrs={'rows': 6, 'cols': 80, 'placeholder': 'При самовывозе можно оставить это поле пустым'}
            ),
            'notice': forms.Textarea(
                attrs={'rows': 6, 'cols': 80}
            ),
        }

    def clean_delivery(self):
        data = self.cleaned_data['delivery']
        if data == 0:
            raise ValidationError('Необходимо выбрать метод доставки')
        return data

    def clean(self):
        if not self.errors:
            delivery = self.cleaned_data['delivery']
            address = self.cleaned_data['address']
            if delivery == 1 and address == '':
                raise ValidationError('Укажите адрес доставки')
        return self.cleaned_data
