from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from shop.forms import SearchForm, OrderModelForm
from shop.models import Product, Manufacturer, Section, Discount, Order


def shop(request):
    result = prerender(request)
    if result:
        return result
    # photos = Photo.objects.all().order_by('-date')[:12]
    products = Product.objects.all().order_by(get_order_by_for_products(request))[:8]
    context = {'products': products,}
    return render(request, 'shop.html', context=context)


def prerender(request):
    if request.GET.get('add_cart'):
        product_id = request.GET.get('add_cart')
        get_object_or_404(Product, pk=product_id)
        cart_info = request.session.get('cart_info', {})
        count = cart_info.get(product_id, 0)
        count += 1
        cart_info.update({product_id: count})
        request.session['cart_info'] = cart_info
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

#
# def gallery(request):
#     photos = Photo.objects.all().order_by('-date')[:12]
#     context ={'photos': photos}
#     # context.update(get_footer_context(request))
#     return render(request, 'gallery.html', context=context)
#
#
def delivery(request):
    return render(request, 'delivery.html')


def contacts(request):
    return render(request, 'contacts.html')


def manufacturer(request, id):
    result = prerender(request)
    if result:
        return result
    current_manufacturer = get_object_or_404(Manufacturer, pk=id)
    products = Product.objects.filter(manufacturer__exact=current_manufacturer).order_by(get_order_by_for_products(request))
    context = {'manufacturer': current_manufacturer, 'products': products}
    return render(request, 'manufacturer.html', context=context)


def section(request, id):
    result = prerender(request)
    if result:
        return result
    current_section = get_object_or_404(Section, pk=id)
    products = Product.objects.filter(section__exact=current_section).order_by(get_order_by_for_products(request))
    context = {'section': current_section, 'products': products}
    return render(request, 'section.html', context=context)


class ProductDetailView(generic.DetailView):
    model = Product

    def get(self, request, *args, **kwargs):
        result = prerender(request)
        if result:
            return result
        return super(ProductDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(section__exact=self.get_object().section).exclude(
            id=self.get_object().id).order_by('?')[:4]
        return context


def get_order_by_for_products(request):
    order_by = ''
    if request.GET.__contains__('sort') and request.GET.__contains__('up'):
        sort = request.GET['sort']
        up = request.GET['up']
        if sort in ('price', 'title'):
            if up == '0':
                order_by = '-'
            order_by += sort
    if not order_by:
        order_by = '-date'
    return order_by


def handler404(request, exception):
    return render(request, '404.html', status=404)


def search(request):
    result = prerender(request)
    if result:
        return result
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        query = search_form.cleaned_data['query']
        products = Product.objects.filter(
            Q(title__icontains=query) |
            # Q(manufacturer__icontains=query) |
            Q(country__icontains=query) |
            Q(description__icontains=query)
        )
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 4)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products.paginator.page(1)
        except EmptyPage:
            products.paginator.page(paginator.num_pages)
        products = paginator.page(page)
        context = {'products': products, 'query': query}
        return render(request, 'sh_search.html', context=context)


def cart(request):
    result = update_cart_info(request)
    if result:
        return result
    cart_info = request.session.get('cart_info')
    products = []
    if cart_info:
        for product_id in cart_info:
            # product = get_object_or_404(Product, pk=product_id)
            try:
                product = Product.objects.get(pk=product_id)
                product.count = cart_info[product_id]
                products.append(product)
            except Product.DoesNotExists:
                raise Http404()
    context = {'products': products, 'discount': request.session.get('discount', '')}
    return render(request, 'cart.html', context=context)


def update_cart_info(request):
    if request.POST:
        cart_info = {}
        for param in request.POST:
            value = request.POST.get(param)
            if param.startswith('count_') and value.isnumeric():
                product_id = param.replace('count_', '')
                get_object_or_404(Product, pk=product_id) # чисто проверка, защита от порченной формы
                cart_info[product_id] = int(value)
            elif param == 'discount' and value:
                try:
                    discount = Discount.objects.get(code__exact=value)
                    request.session['discount'] = value
                except Discount.DoesNotExist:
                    pass
        request.session['cart_info'] = cart_info

    if request.GET.get('delete_cart'):
        product_id = request.GET.get('delete_cart')
        get_object_or_404(Product, pk=product_id)  # чисто проверка, защита от порченной формы
        cart_info = request.session.get('cart_info')
        current_count = cart_info.get(product_id, 0)
        if current_count <= 1:
            cart_info.pop(product_id)
        else:
            cart_info[product_id] -= 1
        request.session['cart_info'] = cart_info
        return HttpResponseRedirect(reverse('cart'))


def order(request):
    cart_info = request.session.get('cart_info')
    if not cart_info:
        raise Http404()
    if request.method == 'POST':
        form = OrderModelForm(request.POST)
        if form.is_valid():
            order_object = Order()
            order_object.needs_delivery = True if form.cleaned_data['delivery'] == 1 else False
            discount_code = request.session.get('discount', '')
            if discount_code:
                try:
                    discount = Discount.objects.get(code__exact=discount_code)
                    order_object.discount = discount
                except Discount.DoesNotExist:
                    pass
            email = request.session.get('email', '')
            if email:
                pass
                # try:
                #     customer = Customer.objects.get(email__exact=email)
                #     order_object.customer = customer
                # except Customer.DoesNotExist:
                #     name = form.cleaned_data['name']
                #     first_name, last_name = name.split()
                #     phone = form.cleaned_data['phone']
                #     email = form.cleaned_data['email']
                #     try:
                #         customer_object = Customer()
                #         customer_object.first_name = first_name
                #         customer_object.last_name = last_name
                #         customer_object.phone = phone
                #         customer_object.email = email
                #         customer_object.save()
                #         order_object.customer = customer_object
                #     except Customer.DoesNotExist:
                #         raise Http404()
            else:
                raise Http404()
            order_object.address = form.cleaned_data['address']
            order_object.notice = form.cleaned_data['notice']
            order_object.save()
            add_order_lines(request, order_object)
            # add_user(name, email)
            return HttpResponseRedirect(reverse('add_order'))
    else:
        form = OrderModelForm()
    context = {'form': form}
    return render(request, 'order.html', context=context)


def add_order_lines(request, order_object):
    cart_info = request.session.get('get_cart_info', {})
    for key in cart_info:
        order_line = OrderLine()
        order_line.order = order_object
        order_line.product = get_object_or_404(Product, pk=key)
        order_line.count = cart_info[key]
        order_line.save()
        # request.session.clear() # cтирает слишком много, в том числе и авторизацию
        del request.session['cart_info']


def add_order(request):
    return render(request, 'add_order.html')
#
# def add_user(name, email):
#     if User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists():
#         return
#
#     password = User.objects.make_random_password()
#     user = User.objects.create_user(email, email, password)
