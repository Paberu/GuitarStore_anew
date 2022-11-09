from django.test import TestCase

from blog.models import Post, Comment


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        post = Post.objects.create(title='Main', subtitle='Submain', slug='slug', author='Клим Чугункин',
                           email='klim@chugun.ru', short_text='Укороченная версия поста',
                           full_text='Увеличенная версия поста, чтоб прям на две страницы, \
                           со всяким говном и палками')
        comment = Comment.objects.create(author='Клим Чугункин', email='klim@chugun.ru',
                                         text='Укороченная версия поста!', post=post)

    # def setUp(self) -> None:
    #     print('setUp вызывается перед каждым тестом')
    #
    # def tearDown(self) -> None:
    #     print('tearDown вызывается после каждого теста')

    def test_author_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('author').max_length
        self.assertEqual(max_length, 100)

    def test_email_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('email').max_length
        self.assertEqual(max_length, 100)

    def test_text_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('text').max_length
        self.assertEqual(max_length, 200)

    def test_parrent_post(self):
        comment = Comment.objects.get(id=1)
        post_id = comment.post.id
        self.assertEqual(post_id, 1)

    def test_subtitle_blank(self):
        post = Post.objects.get(id=1)
        blank = post._meta.get_field('subtitle').blank
        self.assertTrue(blank)