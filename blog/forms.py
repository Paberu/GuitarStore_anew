from django import forms
from django.core.exceptions import ValidationError

from shop.models import SupportMail


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Поиск'}))


class CommentAddingForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Комментарий'}))


class ContactsForm(forms.ModelForm):
    #
    # name = forms.CharField()
    # email = forms.CharField()

    class Meta:
        model = SupportMail
        # fields = ['client_name', 'client_email', 'title', 'text']
        exclude=['date_time']
        help_texts = {
            'name': 'Имя',
            'email': 'E-mail',
            'title': 'Тема',
            'text': 'Сообщение'
        }
        # labels = {}
        # widgets = {
        #     'name': forms.TextInput(attrs={'placeholder': 'Имя'}),
        #     'email': forms.EmailField(),
        #     'title': forms.TextInput(attrs={'placeholder': 'Тема'}),
        #     'text': forms.Textarea(attrs={'placeholder': 'Сообщение'}),
        # }