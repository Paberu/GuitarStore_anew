from django.test import TestCase

from blog.models import Post


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Post.objects.create(title='Main', subtitle='Submain', slug='slug', author='Клим Чугункин',
                           email='klim@chugun.ru', short_text='Укороченная версия поста',
                           full_text='Увеличенная версия поста, чтоб прям на две страницы, \
                           со всяким говном и палками')

    # def setUp(self) -> None:
    #     print('setUp вызывается перед каждым тестом')
    #
    # def tearDown(self) -> None:
    #     print('tearDown вызывается после каждого теста')

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)

    def test_subtitle_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('subtitle').max_length
        self.assertEqual(max_length, 100)

    def test_subtitle_blank(self):
        post = Post.objects.get(id=1)
        blank = post._meta.get_field('subtitle').blank
        self.assertTrue(blank)