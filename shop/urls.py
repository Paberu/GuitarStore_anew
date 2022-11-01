from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    re_path(r'^section/(?P<id>\d+)$', views.section, name='section'),
    re_path(r'^product/(?P<pk>\d+)$', views.ProductDetailView.as_view(), name='product'),
    re_path(r'^manufacturer/(?P<id>\d+)$', views.manufacturer, name='manufacturer'),
    path('delivery', views.delivery, name='delivery'),
    path('contacts', views.contacts, name='contacts'),
    path('search', views.search, name='search'),
    # # re_path(r'^post/(?P<id>\d+)$', views.post, name='post'),
    #
    # path('gallery', views.gallery, name='gallery'),
    # path('second_contacts', views.second_contacts, name='second_contacts'),
    # re_path(r'^blog/$', views.blog_full, name='blog'),
    # re_path(r'^blog/(?P<month_n_year>\w{7})$', views.blog_filtered, name='blog'),
    # path('blog_search', views.blog_search, name='blog_search'),
    path('cart', views.cart, name='cart'),
    path('order', views.order, name='order'),
    # path('add_order', views.add_order, name='add_order'),

]