import uuid
from bs4 import BeautifulSoup
from django.db.models import Q
# from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    Product,
    Category,
    Cart,
    CartItem,
    Country,
)
from .form import UserForm


# Create your views here.
def search_products(products, query):
    if query:
        return products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return products


def index(request, category_slug=None):
    category_page = None
    search_query = request.GET.get('search', None)

    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category_page)
    else:
        products = Product.objects.all()

    products = search_products(products, search_query)

    return render(request, 'index.html', {'products': products, 'category': category_page})


def product_page(request, pk):
    product = Product.objects.get(id=pk)

    soup = BeautifulSoup(product.description,  'html.parser')
    product.description = str(soup)

    images = product.more_image.all()
    return render(request, 'product-page.html', {'product': product, 'slider': images})


def cart_id(request):
    cart = request.session.get(settings.CART_SESSION_ID)
    if not cart:
        cart = request.session[settings.CART_SESSION_ID] = str(uuid.uuid4())
    return cart


def clear_card_id(request):
    del request.session[settings.CART_SESSION_ID]


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(id_cart=cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(id_cart=cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(id_cart=cart_id(request))

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity -= 1
        cart_item.save()

        if cart_item.quantity == 0:
            cart_item.delete()

    except CartItem.DoesNotExist:
        pass

    cart_items_count = CartItem.objects.filter(cart=cart).count()

    if cart_items_count == 0:
        delete_cart(request)

    return redirect('cart')


def delete_cart(request):
    try:
        Cart.objects.get(id_cart=cart_id(request)).delete()
    except Cart.DoesNotExist:
        pass

    return redirect('cart')


def cart(request, total=0, counter=0, cart_items=None):
    country = Country.objects.all()
    try:
        cart = Cart.objects.get(id_cart=cart_id(request))
        if cart.active:
            cart_items = CartItem.objects.filter(cart=cart)
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                counter += cart_item.quantity

    except ObjectDoesNotExist:
        cart = None

    return render(request, 'cart-page.html', {'cart_items': cart_items, 'total': total,
                                              'counter': counter, 'country': country, 'cart': cart})


def new_order(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            cart = Cart.objects.get(id_cart=cart_id(request))
            form.instance.cart_id = cart.id
            form.save()
            cart.active = False
            cart.save()
            clear_card_id(request)

            return redirect('cart')
    else:
        form = UserForm()

    return redirect('cart')