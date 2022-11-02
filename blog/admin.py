from django.contrib import admin

from blog.models import Photo, Comment, Post, SupportMail

admin.site.register(Photo)
admin.site.register(Comment)


class PostDateFilter(admin.SimpleListFilter):
    title = 'Время публикации'
    parameter_name = 'date_time'

    def lookups(self, request, model_admin):
        filters = []
        post = Post.objects.values('date_time').order_by('-date_time')
        if post:
            for post_date in post:
                date = post_date['date_time'].date()
                filter_str = (date.strftime('%m %Y'), date.strftime('%B %Y'))
                if filter_str not in filters:
                    filters.append(filter_str)
        return filters

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        month, year=self.value().split()
        return queryset.filter(date_time__year=year, date_time__month=month)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # readonly_fields = ('display_price', )
    list_display = ('author', 'display_date', 'title')
    list_filter = (PostDateFilter,)
    # fieldsets = (
    #     ('Информация о заказе', {
    #         'fields': ('order',)
    #     }),
    #     ('Информация о данном товаре в заказе', {
    #         'fields': ('product', 'display_price', 'count')
    #     })
    # )

    actions_on_bottom = True
    actions_on_top = False


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


@admin.register(SupportMail)
class SupportMailAdmin(admin.ModelAdmin):
    list_display = ('status', 'date_time', 'name', 'title', 'text')
    list_filter = (SupportMailFilter,)
    actions_on_bottom = True
    actions_on_top = False
    list_per_page = 10
    search_fields = ('name', 'email')
