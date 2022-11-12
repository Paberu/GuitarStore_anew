from django.test import TestCase

from blog.models import Post


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Post.objects.create(title='Main', subtitle='Submain', slug='slug', author='Клим Чугункин',
                           email='klim@chugun.ru', short_text='Укороченная версия поста',
                           full_text='Увеличенная версия поста, чтоб прям на две страницы, \
                           со всяким говном и палками')

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_title_verbose_name(self):
        post = Post.objects.get(id=1)
        verbose_name = post._meta.get_field('title').verbose_name
        self.assertEqual(verbose_name, 'Заголовок')

    def test_title_is_blank(self):
        post = Post.objects.get(id=1)
        self.assertTrue(post._meta.get_field('title').blank)

    def test_subtitle_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('subtitle').max_length
        self.assertEqual(max_length, 100)

    def test_subtitle_verbose_name(self):
        post = Post.objects.get(id=1)
        verbose_name = post._meta.get_field('subtitle').verbose_name
        self.assertEqual(verbose_name, 'Подзаголовок')

    def test_subtitle_is_blank(self):
        post = Post.objects.get(id=1)
        self.assertTrue(post._meta.get_field('subtitle').blank)

    def test_slug_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('slug').max_length
        self.assertEqual(max_length, 40)

    def test_slug_verbose_name(self):
        post = Post.objects.get(id=1)
        verbose_name = post._meta.get_field('slug').verbose_name
        self.assertEqual(verbose_name, 'Псевдоним')

    def test_slug_default(self):
        post = Post.objects.get(id=1)
        default = post._meta.get_field('slug').default
        self.assertEqual(default, '')

    def test_date_time_auto(self):
        post = Post.objects.get(id=1)
        auto_now = post._meta.get_field('date_time').auto_now_add
        self.assertTrue(auto_now)

    def test_date_time_verbose_name(self):
        post = Post.objects.get(id=1)
        verbose_name = post._meta.get_field('date_time').verbose_name
        self.assertEqual(verbose_name, 'Дата добавления поста')

    def test_author_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('author').max_length
        self.assertEqual(max_length, 100)

    def test_author_verbose_name(self):
        post = Post.objects.get(id=1)
        verbose_name = post._meta.get_field('author').verbose_name
        self.assertEqual(verbose_name, 'Автор')

    def test_email_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('email').max_length
        self.assertEqual(max_length, 100)

    def test_short_text_verbose_name(self):
        post = Post.objects.get(id=1)
        verbose_name = post._meta.get_field('short_text').verbose_name
        self.assertEqual(verbose_name, 'Текст для страницы со статьями')

    def test_full_text_verbose_name(self):
        post = Post.objects.get(id=1)
        verbose_name = post._meta.get_field('full_text').verbose_name
        self.assertEqual(verbose_name, 'Полный текст поста')