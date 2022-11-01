from django import template

register = template.Library()


@register.filter(name='blog_date_time')
def blog_date_time(value):
    return 'Размещено {0} в {1}'.format(value.strftime('%d.%m.%Y'), value.strftime('%H:%M'))


@register.filter(name='footer_post_date')
def footer_post_date(value):
    return value.strftime('%d %B %Y')


@register.filter(name='footer_comment_time')
def footer_comment_time(value):
    return value.strftime(' отвечает в {0}'.format(value.strftime('%H:%M')))


# @register.filter(name='declension_of_comments')
# def declension_of_comments(value):
#     suffix = ('комментарий', 'комментария', 'комментариев')
#     keys = (2, 0, 1, 1, 1, 2)
#     mod = value % 100
#     if 9 < mod < 20:
#         suffix_key = 2
#     else:
#         suffix_key = keys[min(mod % 10, 5)]
#     return suffix[suffix_key]