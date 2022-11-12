from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.views import generic

from blog.forms import SearchForm, ContactsForm, RegisterForm
from blog.models import Post, Comment, Photo, SupportMail


def gallery(request):
    photos = Photo.objects.all().order_by('-date')[:12]
    context = {'photos': photos}
    return render(request, 'gallery.html', context=context)


def about(request):
    return render(request, 'about.html')


def blog_full(request):
    posts = Post.objects.all().order_by('-date_time')
    # for post in posts:
    #     slug = transliterate.translit(post.title, reversed=True)
    #     slug = slug.replace("'", '')
    #     slug = slug.replace('?', '')
    #     slug = slug.replace('!', '')
    #     slug = slug.replace(',', '')
    #     slug = slug.replace(' ', '-')
    #     slug = slug.lower()
    #     post.slug = slug
    #     post.save()
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


def contacts(request):
    contacts_form = ContactsForm()
    context = {'contacts_form': contacts_form}
    if request.method == 'POST':
        contacts_form = ContactsForm(request.POST)
        if contacts_form.is_valid():
            support_mail_object = SupportMail()
            support_mail_object.name = contacts_form.cleaned_data['name']
            support_mail_object.email = contacts_form.cleaned_data['email']
            support_mail_object.title = contacts_form.cleaned_data['title']
            support_mail_object.text = contacts_form.cleaned_data['text']
            support_mail_object.save()
            context = {'contacts_form': contacts_form, 'answer': 'Ваше обращение принято. Спасибо за Ваше участие.'}
    return render(request, 'bl_contacts.html', context=context)


class PostDetailView(generic.DetailView):
    model = Post

    def post(self, request, *args, **kwargs):
        author = request.user.first_name + ' ' + request.user.last_name
        email = request.user.email
        post = self.get_object()
        text = request.POST.get('comment')
        Comment.objects.create(author=author, post=post, text=text, email=email)
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


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            result = add_user(first_name, last_name, email, password)
            context = {'message': result}
        else:
            context = {'register_form': register_form}
    else:
        context = {'register_form': RegisterForm()}
    return render(request, 'register.html', context=context)


def add_user(first_name, last_name, email, password):
    if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
        return 'recovery'
    user = User.objects.create_user(email, email, password)
    user.first_name = first_name
    user.last_name = last_name
    group = Group.objects.get(name='Клиенты')
    user.groups.add(group)
    user.save()

    text = get_template('registration/registration_email.html')
    html = get_template('registration/registration_email.html')

    context = {'username': email, 'password': password}

    subject = 'Регистрация'
    from_email = 'noreply@guitarstore.ru'
    text_content = text.render(context)
    html_content = html.render(context)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    return 'success'


@permission_required('blog.can_delete_comments')
def delete_comment(request, id):
    comment_object = get_object_or_404(Comment, pk=id)
    if comment_object.email == request.user.email:
        comment_object.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
