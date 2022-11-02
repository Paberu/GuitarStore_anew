import math

from django.contrib import admin

from shop.models import Section, Manufacturer, FormFactor, Product, Discount, Order, OrderLine, SupportMail

admin.site.register(Section)
admin.site.register(Manufacturer)
admin.site.register(FormFactor)


class PriceFilter(admin.SimpleListFilter):
    title = 'Цена'
    parameter_name = 'price'
    round_value = 50000

    def lookups(self, request, model_admin):
        filters = []
        product = Product.objects.order_by('price').last()
        if product:
            if product.price < self.round_value:
                self.round_value = self.round_value / (10 ** (len(str(self.round_value)) - len(str(product.price))))
            digits_volume = 10 ** (len(str(math.trunc(product.price))) - 1)
            max_price = math.ceil(product.price / digits_volume) * digits_volume
            price = self.round_value
            print(product.price, len(str(math.trunc(product.price))), digits_volume, max_price, price)
            while price <= max_price:
                start = price
                end = '{0} - {1}'.format(price - self.round_value +1, price)
                filters.append((start, end))
                price += self.round_value
        return filters

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        value = int(self.value())
        return queryset.filter(price__gte=(value-self.round_value), price__lte=value)


class SupportMailFilter(admin.SimpleListFilter):
    title = 'Статус обработки'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return SupportMail.STATUSES

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        status_value = self.value()
        return queryset.filter(status=status_value)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'image', 'price', 'date')
    list_filter = ('section', PriceFilter)
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 10
    search_fields = ('title',)


@admin.register(SupportMail)
class SupportMailAdmin(admin.ModelAdmin):
    list_display = ('status', 'date_time', 'client_name', 'title', 'text')
    list_filter = (SupportMailFilter,)
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 10
    search_fields = ('client_name', 'client_email')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'value_percent')
    actions_on_bottom = True
    actions_on_top = False
    # search_fields = ('code','value_percent')

    def save_model(self, request, obj, form, change):
        super(DiscountAdmin, self).save_model(request, obj, form, change)


@admin.register(OrderLine)
class OrderLineAdmin(admin.ModelAdmin):
    readonly_fields = ('display_price', )
    list_display = ('order', 'display_full_title', 'display_price', 'count')
    list_filter = ('order',)
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('order',)
        }),
        ('Информация о данном товаре в заказе', {
            'fields': ('product', 'display_price', 'count')
        })
    )

    actions_on_bottom = True
    actions_on_top = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('display_total_discount', 'customer',
                       'phone', 'email', 'date_order')
    list_display = ('id', 'display_products', 'display_total_discount',
                    'display_amount', 'address', 'notice',
                    'date_order', 'date_send', 'status',
                    'customer', 'phone', 'email')
    list_filter = ('status', 'date_order')
    fieldsets = (
        ('Информация о заказе', {
            'fields': ('needs_delivery', 'discount', 'display_total_discount', 'address', 'notice',)
        }),
        ('Информация о клиенте', {
            'fields': ('customer','display_customer_first_name', 'display_customer_last_name', 'display_customer_phone',
                       'display_customer_email')
        }),
        ('Доставка и оплата', {
            'fields': ('date_order', 'date_send', 'status',)
        })
    )
    date_hierarchy = 'date_order'
    actions_on_bottom = True
    actions_on_top = False
