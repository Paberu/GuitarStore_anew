from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from blog.forms import SearchForm, ContactsForm
from blog.models import Post, Comment, Photo


# def index(request):
#     posts = Post.objects.all().order_by('-date_time')
#     page = request.GET.get('page', 1)
#     paginator = Paginator(posts, 5)
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts.paginator.page(1)
#     except EmptyPage:
#         posts.paginator.page(paginator.num_pages)
#     posts = paginator.page(page)
#     context = {'posts': posts}
#     return render(request, 'blog.html', context=context)


def gallery(request):
    photos = Photo.objects.all().order_by('-date')[:12]
    context ={'photos': photos}
    # context.update(get_footer_context(request))
    return render(request, 'gallery.html', context=context)


def about(request):
    return render(request, 'about.html')


def blog_full(request):
    posts = Post.objects.all().order_by('-date_time')
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 5)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts.paginator.page(1)
    except EmptyPage:
        posts.paginator.page(paginator.num_pages)
    posts = paginator.page(page)
    context = {'posts': posts}
    return render(request, 'blog.html', context=context)


def blog_filtered(request, month_n_year):
    month, year = month_n_year.split('_')
    posts = Post.objects.filter(date_time__year=year, date_time__month=month)
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, 4)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts.paginator.page(1)
    except EmptyPage:
        posts.paginator.page(paginator.num_pages)
    posts = paginator.page(page)
    context = {'posts': posts}
    return render(request, 'blog.html', context=context)


# def post(request, id):
#     current_post = get_object_or_404(Post, pk=id)
#     comments = Comment.objects.filter(post__exact=current_post).order_by('-date_time')
#     comments_total = len(comments)
#     total_lefts = comments_total % 10
#     if 5 < comments_total < 21 or total_lefts > 4:
#         comments_total = str(comments_total) + ' комментариев'
#     elif total_lefts in (2, 3, 4):
#         comments_total = str(comments_total) + ' комментария'
#     else:
#         comments_total = str(comments_total) + ' комментарий'
#     context = {'post': current_post, 'comments': comments, 'comments_total': comments_total}
#     return render(request, 'post.html', context=context)


def contacts(request):
    if request.POST:
        pass
    return render(request, 'bl_contacts.html', context={'form': ContactsForm()})


class PostDetailView(generic.DetailView):
    model = Post

    def post(self, request, *args, **kwargs):
        author = request.POST.get('name')
        email = request.POST.get('email')
        post = self.get_object()
        text = request.POST.get('comment')
        Comment.objects.create(author=author, post=post, text=text)
        request.session['name'] = author
        request.session['email'] = email
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(post__exact=self.get_object()).order_by('-date_time')
        context['comments'] = comments
        comments_total = len(comments)
        total_lefts = comments_total % 10
        if 5 < comments_total < 21 or total_lefts > 4:
            comments_total = str(comments_total) + ' комментариев'
        elif total_lefts in (2, 3, 4):
            comments_total = str(comments_total) + ' комментария'
        else:
            comments_total = str(comments_total) + ' комментарий'
        context['comments_total'] = comments_total
        return context


def handler404(request, exception):
    return render(request, '404.html', status=404)


def search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(subtitle__icontains=query) |
            Q(full_text__icontains=query)
        )
        page = request.GET.get('page', 1)
        paginator = Paginator(posts, 4)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts.paginator.page(1)
        except EmptyPage:
            posts.paginator.page(paginator.num_pages)
        posts = paginator.page(page)
        context = {'posts': posts, 'query': query}
        return render(request, 'bl_search.html', context=context)
