from django.shortcuts import render, get_object_or_404
from django.views.defaults import page_not_found

from core.models import Shop, Checkout, Order, CartItem
from core.utils.payment import Payment

def index(request):
    host = request.headers['host'].split(':')[0]
    context = {
        'shop': get_object_or_404(Shop, domains__contains=[host]),
    }
    return render(request, 'storefront/index.html', context)


def product_details(request, slug=None):
    host = request.headers['host'].split(':')[0]
    shop = get_object_or_404(Shop, domains__contains=[host])
    product = get_object_or_404(shop.products.all(), slug=slug)
    context = {
        'product': product,
        'shop': product.shop
    }
    return render(request, 'storefront/product.html', context)


def product_catalogue(request):
    host = request.headers['host'].split(':')[0]
    shop = get_object_or_404(Shop, domains__contains=[host])
    context = {
        'products': shop.products.all(),
        'shop': shop
    }
    return render(request, 'storefront/products.html', context)

def order_confirmation(request, checkout_uid):
    host = request.headers['host'].split(':')[0]
    shop = get_object_or_404(Shop, domains__contains=[host])
    checkout = get_object_or_404(Checkout, uid=checkout_uid)
    checkout.pay(**request.GET.dict())
    return render(request, 'storefront/order_confirmed.html', {'checkout': checkout, 'shop': shop})

def handle_404(request, exception, template_name="404.html"):
    return page_not_found(request, exception, template_name='storefront/404.html')
