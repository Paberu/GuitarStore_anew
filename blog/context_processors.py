import random
from decimal import Decimal

from blog.forms import SearchForm, CommentAddingForm
from blog.models import Post, Comment, Photo


def add_default_blog_data(request):
    last_comments = Comment.objects.all().order_by('-date_time')[:3]
    for comment in last_comments:
        if len(comment.text) > 150:
            cut_text = comment.text[:150]
            if comment.text[150] == ' ':
                comment.text = cut_text + '...'
            else:
                comment.text = cut_text.rsplit(' ', 1)[0] + '...'
    last_posts = Post.objects.all().order_by('-date_time')[:3]
    small_images = list(Photo.objects.all())
    random_small_images = random.sample(small_images, 6)
    post_dates = Post.objects.values('date_time').order_by('-date_time')
    filters = []
    if post_dates:
        for post_date in post_dates:
            date = post_date['date_time'].date()
            filter_str = {'display_date': date.strftime('%B %Y'), 'month_n_year': date.strftime('%m_%Y')}
            if filter_str not in filters:
                filters.append(filter_str)
    blog_search_form = SearchForm()
    return {'last_comments': last_comments, 'last_posts': last_posts, 'random_small_images': random_small_images,
            'filters': filters, 'blog_search_form': blog_search_form}


def add_default_post_data(request):
    comment_adding_form = CommentAddingForm()
    return {'comment_adding_form': comment_adding_form}