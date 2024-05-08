from django.db import models
from django.urls import reverse
from tinymce import models as tinymce_models

# Create your models here.
STOCK_CHOISE = (
    ('S', 'In stock'),
    ('E', 'Ended'),
    ('D', 'Delivery expected')
)


class Category(models.Model):
    name = models.CharField(max_length=16, verbose_name='Category title')
    slug = models.SlugField(max_length=16)

    def __str__(self) -> str:
        return self.name

    def get_url(self):
        return reverse('product_by_category', args=[self.id])


class Product(models.Model):
    name = models.CharField(max_length=64, verbose_name='Product title')
    slug = models.SlugField(max_length=16)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Product category')
    image = models.ImageField(upload_to=f'', verbose_name='Product image')
    more_image = models.ManyToManyField('SliderImage', blank=True, null=True)
    price = models.FloatField(default=0, verbose_name='Product price')
    description = tinymce_models.HTMLField(verbose_name='Product description')
    country = models.ForeignKey('Country', on_delete=models.CASCADE, verbose_name='Product country')
    width = models.FloatField(default=0, verbose_name='Width')
    height = models.FloatField(default=0, verbose_name='Height')
    length = models.FloatField(default=0, verbose_name='Length')
    author = models.CharField(max_length=64, verbose_name='Author')
    color = models.ManyToManyField('Color', verbose_name='Product colors')
    page_number = models.IntegerField(default=0, verbose_name='Page number')
    stock = models.CharField(max_length=1, choices=STOCK_CHOISE, verbose_name='Stock')
    quantity_product = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            product_name = self.name[:5]
            file_extension = self.image.name.split('.')[-1]
            new_image_name = f"{product_name}.{file_extension}"
            self.image.name = new_image_name
        super().save(*args, **kwargs)

    def get_url(self) -> int:
        return reverse('product', args=[self.id])


class SliderImage(models.Model):
    image = models.ImageField(upload_to='product_image/')


class Country(models.Model):
    name = models.CharField(max_length=32, verbose_name='Country name')
    slug = models.SlugField(max_length=16)

    def __str__(self) -> str:
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=16, verbose_name='Color name')
    hex = models.CharField(max_length=16, verbose_name='Hex color')

    def __str__(self) -> str:
        return self.name


class Cart(models.Model):
    id_cart = models.CharField(max_length=256, blank=True)
    active = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id_cart)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str(self.product)


class DeliveryMethod(models.Model):
    post_name = models.CharField(max_length=32, unique=True)
    delivery_coast = models.FloatField()

    def __str__(self):
        return self.post_name


class Order(models.Model):
    order_id = models.CharField(max_length=32, blank=True, null=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=16)
    email = models.EmailField()
    # delivery_method = models.ForeignKey()
    address = models.CharField(max_length=256)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # pay = models.BooleanField(default=False)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.pay is True:
            pass

