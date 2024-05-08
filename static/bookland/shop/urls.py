from django.urls import path
from .views import (
    index, 
    product_page,
    cart,
    add_cart,
    delete_cart,
    remove_cart,
    new_order
)

urlpatterns = [
    path('', index, name='index'),
    path('<slug:category_slug>', index, name='product_by_category'),
    path('product/<int:pk>/', product_page, name='product'),
    path('cart/', cart, name='cart'),
    path('cart/add/<int:product_id>/', add_cart, name='add_cart'),
    path('cart/delete/', delete_cart, name='delete_cart'),
    path('cart/remove/<int:product_id>/', remove_cart, name='remove_cart'),
    path('cart/order/', new_order, name='new_order')
]