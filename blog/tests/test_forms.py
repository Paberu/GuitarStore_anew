from django.test import TestCase

from blog.forms import SearchForm, ContactsForm, RegisterForm, CommentAddingForm
from blog.models import SupportMail


class SearchFormTest(TestCase):

    def test_query_placeholder(self):
        form = SearchForm()
        self.assertEqual(form.fields['query'].widget.attrs['placeholder'], 'Поиск')

    def test_good_search(self):
        data = {'query': 'Гитарный'}
        form = SearchForm(data)
        self.assertTrue(form.is_valid())


class CommentAddingFormTest(TestCase):

    def test_name_placeholder(self):
        form = CommentAddingForm()
        self.assertEqual(form.fields['name'].widget.attrs['placeholder'], 'Имя')

    def test_email_placeholder(self):
        form = CommentAddingForm()
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Email')

    def test_comment_placeholder(self):
        form = CommentAddingForm()
        self.assertEqual(form.fields['comment'].widget.attrs['placeholder'], 'Комментарий')

    def test_normal_adding(self):
        data = {'name': 'Имя', 'email': 'erf@asde.ru', 'comment': 'Пространный комментарий'}
        form = CommentAddingForm(data)
        self.assertTrue(form.is_valid())

    def test_bad_adding_name(self):
        data = {'name': '', 'email': 'erf@asde.ru', 'comment': 'Пространный комментарий'}
        form = CommentAddingForm(data)
        self.assertFalse(form.is_valid())

    def test_bad_adding_email(self):
        data = {'name': 'Вася', 'email': 'erfasde.ru', 'comment': 'Пространный комментарий'}
        form = CommentAddingForm(data)
        self.assertFalse(form.is_valid())

    def test_bad_adding_comment(self):
        data = {'name': 'Вася', 'email': 'erfa@de.ru', 'comment': ''}
        form = CommentAddingForm(data)
        self.assertFalse(form.is_valid())

    def test_bad_adding_space_comment(self):
        data = {'name': 'Вася', 'email': 'erfa@de.ru', 'comment': '     '}
        form = CommentAddingForm(data)
        self.assertFalse(form.is_valid())


class ContactsFormTest(TestCase):

    def test_model(self):
        form = ContactsForm()
        self.assertEqual(form._meta.model, SupportMail)

    def test_excludes(self):
        form = ContactsForm()
        self.assertEqual(form._meta.exclude, ['date_time', 'status'])

    def test_help_texts(self):
        form = ContactsForm()
        data = {'name': 'Имя', 'email': 'E-mail', 'title': 'Тема', 'text': 'Сообщение'}
        self.assertEqual(form._meta.help_texts, data)

    def test_good_adding(self):
        data = {'name': 'Имя', 'email': 'email@fd.com', 'title': 'Тема', 'text': 'Сообщение'}
        form = ContactsForm(data)
        self.assertTrue(form.is_valid())

    def test_bad_adding_name(self):
        data = {'name': '', 'email': 'email@fd.com', 'title': 'Тема', 'text': 'Сообщение'}
        form = ContactsForm(data)
        self.assertFalse(form.is_valid())

    def test_bad_adding_not_email(self):
        data = {'name': 'Коля', 'email': 'sdfedfd.cf', 'title': 'Тема', 'text': 'Сообщение'}
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_bad_adding_email(self):
        data = {'name': 'Коля', 'email': '', 'title': 'Тема', 'text': 'Сообщение'}
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_bad_adding_title(self):
        data = {'name': 'Имя', 'email': 'email@fd.com', 'title': '', 'text': 'Сообщение'}
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_bad_adding_text(self):
        data = {'name': 'Имя', 'email': 'email@fd.com', 'title': 'Тема', 'text': ''}
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())


class RegisterFormTest(TestCase):

    def test_first_name_placeholder(self):
        form = RegisterForm()
        self.assertEqual(form.fields['first_name'].widget.attrs['placeholder'], 'Имя')

    def test_last_name_placeholder(self):
        form = RegisterForm()
        self.assertEqual(form.fields['last_name'].widget.attrs['placeholder'], 'Фамилия')

    def test_email_placeholder(self):
        form = RegisterForm()
        self.assertEqual(form.fields['email'].widget.attrs['placeholder'], 'Email')

    def test_password_placeholder(self):
        form = RegisterForm()
        self.assertEqual(form.fields['password'].widget.attrs['placeholder'], 'Пароль')

    def test_password_repeat_placeholder(self):
        form = RegisterForm()
        self.assertEqual(form.fields['password_repeat'].widget.attrs['placeholder'], 'Повторите пароль')

    def test_good_form(self):
        data = {'first_name': 'Коля', 'last_name': 'Николаев', 'email': 'sdfe@dfd.cf', 'password': '2kd03ifke',
                'password_repeat': '2kd03ifke'}
        form = RegisterForm(data)
        self.assertTrue(form.is_valid())

    def test_bad_adding_first_name(self):
        data = {'first_name': '', 'last_name': 'Николаев', 'email': 'sdfe@dfd.cf', 'password': '2kd03ifke',
                'password_repeat': '2kd03ifke'}
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_bad_adding_last_name(self):
        data = {'first_name': 'Коля', 'last_name': '', 'email': 'sdfe@dfd.cf', 'password': '2kd03ifke',
                'password_repeat': '2kd03ifke'}
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_bad_adding_not_email(self):
        data = {'first_name': 'Коля', 'last_name': 'Иванов', 'email': 'sdfedfd.cf', 'password': '2kd03ifke',
                'password_repeat': '2kd03ifke'}
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_bad_adding_email(self):
        data = {'first_name': 'Коля', 'last_name': 'Иванов', 'email': '', 'password': '2kd03ifke',
                'password_repeat': '2kd03ifke'}
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_short_password(self):
        data = {'first_name': 'Коля', 'last_name': 'Иванов', 'email': '', 'password': '123',
                'password_repeat': '123'}
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_non_match_password(self):
        data = {'first_name': 'Коля', 'last_name': 'Иванов', 'email': '', 'password': '12345',
                'password_repeat': '54321'}
        form = RegisterForm(data)
        self.assertFalse(form.is_valid())
