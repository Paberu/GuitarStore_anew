from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    # re_path(r'^section/(?P<id>\d+)$', views.section, name='section'),
    # re_path(r'^product/(?P<pk>\d+)$', views.ProductDetailView.as_view(), name='product'),
    # re_path(r'^manufacturer/(?P<id>\d+)$', views.manufacturer, name='manufacturer'),
    path('section/<slug:slug>', views.section, name='section'),
    path('product/<slug:slug>', views.ProductDetailView.as_view(), name='product'),
    path('manufacturer/<slug:slug>', views.manufacturer, name='manufacturer'),
    path('delivery', views.delivery, name='delivery'),
    path('contacts', views.contacts, name='contacts'),
    path('search', views.search, name='search'),
    path('cart', views.cart, name='cart'),
    path('order', views.order, name='order'),
    path('add_order', views.add_order, name='add_order'),
    path('orders', views.orders, name='orders'),
    re_path(r'^cancel_order/(?P<id>\d+)$', views.cancel_order, name='cancel_order'),

]