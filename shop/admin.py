from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (
    Category,
    Product,
    Country,
    Color,
    SliderImage,
    Cart,
    CartItem,
    Order,
    DeliveryMethod
)

# Register your models here.
admin.site.register(Category)


@admin.action(description="Choice to the stock")
def stock(modeladmin, request, queryset):
    queryset.update(stock="S")


@admin.action(description="Choice to the ended")
def ended(modeladmin, request, queryset):
    queryset.update(stock="E")


@admin.action(description="Choice to the delivery expected")
def delivery(modeladmin, request, queryset):
    queryset.update(stock="D")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'img', 'category', 'price', 'stock']
    actions = [stock, ended, delivery]

    def img(self, obj):
        if obj.image:
            return mark_safe('<img src="{}"  width=60 />'.format(obj.image.url))


admin.site.register(Country)
admin.site.register(Color)
admin.site.register(SliderImage)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(DeliveryMethod)
