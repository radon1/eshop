from django.db import models
from django.urls import reverse
from django.utils.html import format_html_join, format_html
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver



class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    name = models.CharField('Название', max_length=150)
    slug = models.SlugField(max_length=150)
    gallery = models.ManyToManyField('photologue.Gallery', verbose_name='Галерея')
    description = models.TextField('Описание')
    image = models.ImageField(verbose_name='Фотография', blank=True, upload_to='shop/')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    #price_2 = models.IntegerField('Цена_2', default=0)
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=0)
    color = models.CharField('Цвет', max_length=100)
    availability = models.BooleanField(default=True, verbose_name='Наличие')
    detailed_description = models.TextField('Детальное описание')
    rank = models.FloatField(verbose_name='Рейтинг', default=0)
    discount = models.PositiveIntegerField(verbose_name='Скидка', default=0)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={"slug": self.slug})

class Gallery(models.Model):
    name = models.CharField('Название', max_length=150)
    image = models.ImageField(verbose_name='Фото', blank=True, upload_to='gallery/')

    class Meta:
        verbose_name = 'Галерея'
        verbose_name_plural = 'Галерея'

    def __str__(self):
        return self.name


class Cart(models.Model):
    '''Корзина'''
    user = models.ForeignKey(User, verbose_name='Покупатель', 	on_delete=models.CASCADE)
    accepted = models.BooleanField(verbose_name='Принято к заказу', default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return "{}".format(self.user)


class CartItem(models.Model):
    '''Товары в корзине'''
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Количество', default=1)
    price_sum = models.PositiveIntegerField('Общая сумма', default=0)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return "{}".format(self.cart)

    def save(self, *args, **kwargs):
        self.price_sum = self.quantity * self.product.price
        super().save(*args, **kwargs)


class Order(models.Model):
    '''Заказы'''
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE)
    accepted = models.BooleanField(verbose_name='Заказ выполнен', default=False)
    date = models.DateTimeField('Дата', default=timezone.now)

    def products_list(self):
        products = CartItem.objects.filter(cart=self.cart)
        items = format_html_join(
            "\n",
            """
                    <tr>
                        <td style="width:50%">{0}</td>
                        <td style="width:50%">{1}</td>
                    </tr>
            """,
            ((product.product.name, product.quantity) for product in products)
        )
        return format_html("""<table style="width:100%">
                    <colgroup>
                        <col span="2" style="background:Khaki;">
                        <col style="background-color:Cyan;">
                    </colgroup>
                    <tr><th>Наименование</th><th>Количество</th></tr> {} </table>""", items)

    products_list.short_description = 'Products List'
    products_list.allow_tags = True

    def get_user(self):
        return "{}".format(self.user.username)

    get_user.short_description = 'Get User'
    get_user.allow_tags = True


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return "{}".format(self.cart)



@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    '''Создание корзины пользователя'''
    if created:
        Cart.objects.create(user=instance)
