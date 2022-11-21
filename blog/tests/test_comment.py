from django.test import TestCase

from blog.models import Post, Comment


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        post = Post.objects.create(title='Main', subtitle='Submain', slug='slug', author='Клим Чугункин',
                                   email='klim@chugun.ru', short_text='Укороченная версия поста',
                                   full_text='Увеличенная версия поста, чтоб прям на две страницы, \
                           со всяким говном и палками')
        Comment.objects.create(author='Клим Чугункин', email='klim@chugun.ru',
                               text='Укороченная версия поста!', post=post)

    def test_author_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('author').max_length
        self.assertEqual(max_length, 100)

    def test_author_verbose(self):
        comment = Comment.objects.get(id=1)
        verbose = comment._meta.get_field('author').verbose_name
        self.assertEqual(verbose, 'Автор')

    def test_email_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('email').max_length
        self.assertEqual(max_length, 100)

    def test_email_verbose(self):
        comment = Comment.objects.get(id=1)
        verbose = comment._meta.get_field('email').verbose_name
        self.assertEqual(verbose, 'E-mail')

    def test_text_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('text').max_length
        self.assertEqual(max_length, 200)

    def test_text_verbose(self):
        comment = Comment.objects.get(id=1)
        verbose = comment._meta.get_field('text').verbose_name
        self.assertEqual(verbose, 'Содержимое комментария')

    def test_parent_post(self):
        comment = Comment.objects.get(id=1)
        post_id = comment.post.id
        self.assertEqual(post_id, 1)
