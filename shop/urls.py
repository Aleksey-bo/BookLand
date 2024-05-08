from django.urls import path
from .views import (
    PreviewProduct,
    ProductPage,
    CartView,
    AddToCart,
    CartDeleteView,
    RemoveProductView,
    FormForOrder
)

urlpatterns = [
    path('', PreviewProduct.as_view(), name='index'),
    path('<int:id>/', PreviewProduct.as_view(), name='product_by_category'),
    path('product/<int:pk>/', ProductPage.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/delete/', CartDeleteView.as_view(), name='delete_cart'),
    path('cart/remove/<int:product_id>/', RemoveProductView.as_view(), name='remove_product'),
    path('cart/user_form/', FormForOrder.as_view(), name='new_order')
]
