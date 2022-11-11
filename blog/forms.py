from django import forms
from django.core.exceptions import ValidationError

from blog.models import SupportMail


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Поиск'}))


class CommentAddingForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Комментарий'}))


class ContactsForm(forms.ModelForm):

    class Meta:
        model = SupportMail
        exclude=['date_time', 'status']
        help_texts = {
            'name': 'Имя',
            'email': 'E-mail',
            'title': 'Тема',
            'text': 'Сообщение'
        }


class RegisterForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Фамилия'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Повторите пароль'}))

    def clean_password(self):
        data = self.cleaned_data['password']
        if len(data) < 5:
            raise ValidationError('Ваш пароль слишком простой')
        return data

    def clean(self):
        if not self.errors:
            password = self.cleaned_data['password']
            password_repeat = self.cleaned_data['password_repeat']
            if password != password_repeat:
                raise ValidationError('Пароли должны совпадать')
        return self.cleaned_data
