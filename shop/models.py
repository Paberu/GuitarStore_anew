import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class Discount(models.Model):
    code = models.CharField(max_length=13, verbose_name='Код купона')
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)],
        verbose_name='Размер скидки',
        help_text='В процентах'
    )

    class Meta:
        ordering = ['-value']
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'

    def value_percent(self):
        return str(self.value)+'%'

    def __str__(self):
        return '{0} ({1}%)'.format(self.code, str(self.value))

    value_percent.short_description = 'Размер скидки'


class Section(models.Model):
    title = models.CharField(
        max_length=70,
        help_text='Здесь надо вводить название раздела',
        unique=True,
        verbose_name='Название раздела'
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def get_absolute_url(self):
        return reverse('section', args=[self.id])

    def __str__(self):
        return self.title


class Manufacturer(models.Model):
    title = models.CharField(
        max_length=70,
        help_text='Здесь надо вводить название производителя',
        unique=True,
        verbose_name='Название производителя'
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def get_absolute_url(self):
        return reverse('manufacturer', args=[self.id])

    def __str__(self):
        return self.title


class FormFactor(models.Model):
    title = models.CharField(
        max_length=70,
        help_text='Здесь надо вводить тип гитары (или оставить пустым, если аксессуар)',
        unique=True,
        verbose_name='Название типа гитары'
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Форм-фактор'
        verbose_name_plural = 'Форм-факторы'

    def __str__(self):
        return self.title


class Product(models.Model):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, verbose_name='Раздел')
    title = models.CharField(max_length=70, verbose_name='Название товара')
    image = models.ImageField(upload_to='images', verbose_name='Изображение')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True, verbose_name='Производитель')
    year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year)],
        verbose_name='Год'
    )
    country = models.CharField(max_length=70, verbose_name='Страна')
    description = models.TextField(verbose_name="Описание")
    date = models.DateField(auto_now_add=True, verbose_name='Дата добавления')

    count = 1

    class Meta:
        ordering = ['title', 'year']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_count(self):
        return self.count

    def get_sum_price(self):
        return self.price * self.count

    def __str__(self):
        return '{0} ({1})'.format(self.title, self.section.title)


class Order(models.Model):
    needs_delivery = models.BooleanField(verbose_name='Необходима доставка')
    discount = models.ForeignKey(Discount, verbose_name='Скидка', on_delete=models.SET_NULL, null=True)
    customer = models.CharField(max_length=100, verbose_name='Клиент')
    address = models.TextField(verbose_name='Адрес', blank=True)
    notice = models.CharField(max_length=200, blank=True, verbose_name='Примечание пользователя к заказу')
    date_order = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время заказа')
    date_send = models.DateTimeField(null=True, blank=True, verbose_name='Дата и время отправки')

    STATUSES = (
        ('NEW', 'Новый заказ'),
        ('APR', 'Подтвержден'),
        ('PAY', 'Оплачен'),
        ('CNL', 'Отменён'),
        ('MDP', 'Сформирован'),
        ('SND', 'Отправлен'),

    )

    status = models.CharField(choices=STATUSES, max_length=3, default='NEW', verbose_name='Статус заказа')

    class Meta:
        ordering = ['-date_order']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'ID: ' + str(self.id)

    def display_total_discount(self):
        total_discount = 0
        if self.customer.discount:
            total_discount += self.customer.discount.value
        if self.discount:
            total_discount += self.discount.value
        if total_discount > 99:
            return 99
        return total_discount

    def display_products(self):
        display = ''
        for orderline in self.orderline_set.all():
            display += '{0}: {1} шт.; '.format(orderline.product.title, orderline.count)
        return display

    def display_amount(self):
        amount = 0
        for orderline in self.orderline_set.all():
            amount += orderline.product.price * orderline.count
        if self.discount:
            amount = round(amount * (100 - self.display_total_discount()) / 100)
        return '{0} руб.'.format(amount)

    def display_customer_first_name(self):
        return self.customer.first_name

    def display_customer_last_name(self):
        return self.customer.last_name

    def display_customer_phone(self):
        return self.customer.phone

    def display_customer_email(self):
        return self.customer.email

    display_products.short_description = 'Состав заказа'
    display_amount.short_description = 'Цена заказа'
    display_total_discount.short_description = 'Общий размер скидки'
    display_customer_first_name.short_description = 'Имя заказчика'
    display_customer_last_name.short_description = 'Фамилия заказчика'
    display_customer_phone.short_description = 'Телефон заказчика'
    display_customer_email.short_description = 'Email заказчика'


class OrderLine(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена', default=0)
    count = models.IntegerField(verbose_name='Количество', validators=[MinValueValidator(1)], default=1)

    class Meta:
        verbose_name = 'Строка заказа'
        verbose_name_plural = 'Строки заказа'

    def __str__(self):
        return 'Заказ (ID {0}) {1}: {2} шт.'.format(self.order.id, self.product.title, self.count)

    def display_full_title(self):
        return '{0} ({1})'.format(self.product.title, self.product.section.title)

    def display_price(self):
        return self.product.price

    display_full_title.short_description = 'Товар'
    display_price.short_description = 'Цена за единицу товара'


class SupportMail(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок', blank=True)
    text = models.TextField(verbose_name='Содержимое обращения')
    # customer = models.ForeignKey(Customer, verbose_name='Клиент', on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата обращения')
    client_name = models.CharField(max_length=100, verbose_name='Имя')
    client_email = models.EmailField(max_length=100, verbose_name='E-mail')

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
        # fullname = '{0} {1} {2}'.format(self.customer.first_name, self.customer.middle_name, self.customer.last_name)
        return 'Клиент {0} обратился {1} с запросом: {2}'.format(self.client_name, self.date_time.date(), self.title)


class Comment(models.Model):
    product = models.ForeignKey(Product, verbose_name='Комментарий', on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время добавления коммента')
    author = models.CharField(max_length=100, verbose_name='Автор')
    text = models.TextField(max_length=200, verbose_name='Содержимое комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return '{0} {1} оставил комментарий: {2}'.format(self.author, self.date_time.date(), self.text)

    def display_date(self):
        return self.date_time.date().strfdate('%d %B, %Y')
