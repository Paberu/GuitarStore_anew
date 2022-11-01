from django import forms
from django.core.exceptions import ValidationError

from shop.models import Order, SupportMail


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Поиск'}))


class CommentAddingForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Комментарий'}))


class OrderModelForm(forms.ModelForm):
    name = forms.CharField(label='ФИО')
    phone = forms.CharField(label='Телефон')
    email = forms.CharField(label='E-mail')

    DELIVERY_CHOICES = (
        (0, 'Выберите, пожалуйста'),
        (1, 'Доставка'),
        (2, 'Самовывоз'),
    )
    delivery = forms.TypedChoiceField(label='Доставка', choices=DELIVERY_CHOICES, coerce=int)
    # address = forms.CharField(label='Полный адрес доставки, шурум-бурум', widget=forms.Textarea(attrs={'rows': 6, 'cols': 80, 'placeholder': 'При самовывозе можно оставить это поле пустым'}))
    # notice = forms.CharField(label='Примечание к заказу', widget=forms.Textarea(attrs={'rows': 6, 'cols': 80}))

    class Meta:
        model = Order
        # exclude = ['discount', 'needs_delivery', 'status']
        fields = ['name', 'phone', 'email', 'delivery', 'address', 'notice']
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
        delivery = self.cleaned_data['delivery']
        address = self.cleaned_data['address']
        if delivery == 1 and address == '':
            raise ValidationError('Укажите адрес доставки')
        return self.cleaned_data
