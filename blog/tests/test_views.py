from django.test import TestCase

from blog.models import Post, Comment, Photo


class BlogViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        post1 = Post.objects.create(title='Main', subtitle='Submain', slug='slug', author='Клим Чугункин',
                           email='klim@chugun.ru', short_text='Укороченная версия поста',
                           full_text='Увеличенная версия поста, чтоб прям на две страницы, \
                           со всяким говном и палками')

        post2 = Post.objects.create(title='Main2', subtitle='Submain2', slug='slug2', author='Клим Чугункин',
                            email='klim@chugun.ru', short_text='Укороченная версия поста 2',
                            full_text='Увеличенная версия поста 2, чтоб прям на две страницы, \
                           со всяким говном и палками, AAAAA!')

        Comment.objects.create(author='Вася', email='vasya@v.ru', text='ЫЫЫЫ!', post=post1)
        Comment.objects.create(author='Вася', email='vasya@v.ru', text='ЫЫЫЫ!', post=post1)
        Comment.objects.create(author='Вася', email='vasya@v.ru', text='УУУУУ!', post=post1)
        Comment.objects.create(author='Вася', email='vasya@v.ru', text='УУУУУ!', post=post2)
        Comment.objects.create(author='Вася', email='vasya@v.ru', text='УУУУУ!', post=post2)
        Comment.objects.create(author='Вася', email='vasya@v.ru', text='УУУУУ!', post=post2)

        for i in range(8):
            Photo.objects.create(title='title'+str(i), image='images/3s37mxl39462khqwj0jzf2g366mtmb8i_alvFJcD.webp',
                                 description='')

    def test_200(self):
        responce = self.client.get('/blog/')
        self.assertEqual(responce.status_code, 200)

    def test_template(self):
        responce = self.client.get('/blog/')
        self.assertTemplateUsed(responce, 'blog.html')

    def test_context(self):
        responce = self.client.get('/blog/')
        self.assertEqual(len(responce.context['random_small_images']), 6)
        self.assertEqual(len(responce.context['posts']), 2)


class GalleryViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        post1 = Post.objects.create(title='Main', subtitle='Submain', slug='slug', author='Клим Чугункин',
                           email='klim@chugun.ru', short_text='Укороченная версия поста',
                           full_text='Увеличенная версия поста, чтоб прям на две страницы, \
                           со всяким говном и палками')

        post2 = Post.objects.create(title='Main2', subtitle='Submain2', slug='slug2', author='Клим Чугункин',
                            email='klim@chugun.ru', short_text='Укороченная версия поста 2',
                            full_text='Увеличенная версия поста 2, чтоб прям на две страницы, \
                           со всяким говном и палками, AAAAA!')

        Comment.objects.create(author='Вася', email='vasya@v.ru', text='ЫЫЫЫ!', post=post1)
        Comment.objects.create(author='Вася', email='vasya@v.ru', text='ЫЫЫЫ!', post=post1)
        Comment.objects.create(author='Вася', email='vasya@v.ru', text='УУУУУ!', post=post1)
        Comment.objects.create(author='Вася', email='vasya@v.ru', text='УУУУУ!', post=post2)
        Comment.objects.create(author='Вася', email='vasya@v.ru', text='УУУУУ!', post=post2)
        Comment.objects.create(author='Вася', email='vasya@v.ru', text='УУУУУ!', post=post2)

        for i in range(16):
            Photo.objects.create(title='title'+str(i), image='images/3s37mxl39462khqwj0jzf2g366mtmb8i_alvFJcD.webp',
                                 description='')

        def test_200(self):
            responce = self.client.get('/blog/gallery/')
            self.assertEqual(responce.status_code, 200)

        def test_template(self):
            responce = self.client.get('/blog/gallery/')
            self.assertTemplateUsed(responce, 'gallery.html')

        def test_context(self):
            responce = self.client.get('/blog/gallery/')
            self.assertEqual(len(responce.context['random_small_images']), 6)
            self.assertEqual(len(responce.context['last_posts']), 2)
            self.assertEqual(len(responce.context['last_comments']), 3)
            self.assertEqual(len(responce.context['photos']), 12)
