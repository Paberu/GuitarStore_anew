from django.urls import path, re_path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_full, name='index'),
    re_path(r'^blog/$', views.blog_full, name='blog'),
    re_path(r'^blog/(?P<month_n_year>\w{7})$', views.blog_filtered, name='blog'),
    # re_path(r'^post/(?P<pk>\d+)$', views.PostDetailView.as_view(), name='post'),
    path('post/<slug:slug>', views.PostDetailView.as_view(), name='post'),
    path('gallery', views.gallery, name='gallery'),
    path('about', views.about, name='about'),
    path('contacts', views.contacts, name='contacts'),
    path('search', views.search, name='search'),
    path('register', views.register, name='register'),
    re_path(r'^delete_comment/(?P<id>\d+)$', views.delete_comment, name='delete_comment'),
]