from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок', blank=True)
    subtitle = models.CharField(max_length=100, verbose_name='Подзаголовок', blank=True)
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления поста')
    author = models.CharField(max_length=100, verbose_name='Автор')
    short_text = models.TextField(verbose_name='Текст для страницы со статьями')
    full_text = models.TextField(verbose_name='Полный текст поста')

    class Meta:
        ordering = ['date_time']
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def display_date(self):
        return self.date_time.date()

    def __str__(self):
        return '{0} {1} написал следующую статью: {2}'.format(self.author, self.date_time, self.title)


class Comment(models.Model):
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления коммента')
    author = models.CharField(max_length=100, verbose_name='Автор')
    text = models.TextField(max_length=200, verbose_name='Содержимое комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Пост')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return '{0} {1} оставил комментарий: {2}'.format(self.author, self.date_time, self.text)


class Photo(models.Model):
    title = models.CharField(max_length=70, verbose_name='Название фотографии')
    image = models.ImageField(upload_to='images', verbose_name='Изображение')
    description = models.TextField(verbose_name="Описание", blank=True)
    date = models.DateField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        ordering = ['-date', 'title']
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def __str__(self):
        return self.title


class SupportMail(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок', blank=True)
    text = models.TextField(verbose_name='Содержимое обращения')
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата обращения')
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(max_length=100, verbose_name='E-mail')

    STATUSES = (
        ('WCH', 'Обращение рассмотрено'),
        ('UNW', 'Обращение нерассмотрено'),
    )

    status = models.CharField(choices=STATUSES, max_length=3, default='UNW', verbose_name='Статус обращения')

    class Meta:
        ordering = ['-date_time']
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'

    def __str__(self):
        return 'Клиент {0} обратился {1} с запросом: {2}'.format(self.name, self.date_time.date(), self.title)
