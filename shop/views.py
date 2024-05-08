import uuid

from bs4 import BeautifulSoup
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DeleteView, DetailView
from django_filters.views import FilterView
from django.views.generic.edit import FormView
from django.shortcuts import redirect, render
from .models import (
    Product,
    Category,
    Country,
    Cart,
    CartItem,
)
from .form import UserForm


def search_products(products, query):
    if query:
        return products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return products


class PreviewProduct(ListView):
    template_name = 'index.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs.get('id')
        search_query = self.request.GET.get('search', None)
        if category_id:
            category = Category.objects.get(id=category_id)
            products = Product.objects.filter(category=category)
        else:
            filter_condition = Q(stock='S') | Q(stock='E')
            products = Product.objects.filter(filter_condition)

        products = search_products(products, search_query)
        return products


class ProductPage(DetailView):
    model = Product
    template_name = 'product-page.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')

        product = Product.objects.get(id=pk)

        soup = BeautifulSoup(product.description, 'html.parser')
        product.description = str(soup)

        images = product.more_image.all()

        context['product'] = product
        context['slider'] = images

        return context


def get_cart(request):
    cart = request.session.get(settings.CART_SESSION_ID)
    if not cart:
        cart = request.session[settings.CART_SESSION_ID] = str(uuid.uuid4())
    return cart


def clear_cart_id(request):
    del request.session[settings.CART_SESSION_ID]


class CartView(View):
    def get(self, *args, **kwargs):
        country = Country.objects.all()
        cart_items = None
        try:
            cart = Cart.objects.get(id_cart=get_cart(self.request))
            if cart.active:
                cart_items = CartItem.objects.filter(cart=cart)

        except ObjectDoesNotExist:
            cart = None

        return render(self.request, 'cart-page.html', {'cart_items': cart_items, 'cart': cart, 'country': country})


class AddToCart(View):
    def get(self, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['product_id'])

        try:
            cart = Cart.objects.get(id_cart=get_cart(self.request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(id_cart=get_cart(self.request))
            cart.save()

        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            cart_item.quantity += 1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem(product=product, cart=cart, quantity=1)
            cart_item.save()

        return redirect('cart')


class RemoveProductView(View):
    def get(self, *args, **kwargs):
        product = Product.objects.get(id=self.kwargs['product_id'])
        cart = Cart.objects.get(id_cart=get_cart(self.request))

        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity -= 1
        cart_item.save()

        if cart_item.quantity == 0:
            cart_item.delete()

        cart_items_count = CartItem.objects.filter(cart=cart).count()

        if cart_items_count == 0:
            return redirect('delete_cart')

        return redirect('cart')


class CartDeleteView(DeleteView):
    model = Product
    template_name = 'cart-page.html'
    success_url = reverse_lazy('cart')

    def get_object(self, queryset=None):
        try:
            cart_id = get_cart(self.request)
            Cart.objects.get(id_cart=cart_id).delete()
        except Cart.DoesNotExist as e:
            print(f"Error: {e}")
        finally:
            return redirect('cart')


class FormForOrder(FormView):
    template_name = 'cart-page.html'
    form_class = UserForm
    success_url = reverse_lazy('cart')

    def form_valid(self, form):
        cart = Cart.objects.get(id_cart=get_cart(self.request))
        cart_items = CartItem.objects.filter(cart=cart)

        for cart_item in cart_items:
            try:
                cart_item.product.quantity_product -= cart_item.quantity
            except ValueError:
                print('Error')

            if cart_item.product.quantity_product <= 0:
                cart_item.product.stock = 'D'
            elif cart_item.product.quantity_product <= 5:
                cart_item.product.stock = 'E'

            cart_item.product.save()

        form.instance.cart_id = cart.id
        form.save()
        cart.active = False
        cart.save()
        clear_cart_id(self.request)
        return super().form_valid(form)
