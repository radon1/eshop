from django.test import TestCase
from django.urls import reverse

from shop.models import Product, Category
from . import views
from . import models


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        category = Category.objects.create(name='category', slug='category')
        Product.objects.create(name='TV', category=category, slug='tv',
                               description='Описание', price='29999', quantity='50',
                               color='black', availability='True', detailed_description='Детальное описание',
                               rank='5', discount='10')

    def test_view_url_exists_at_desired_location(self):
        product = Product.objects.get(id=1)
        resp = self.client.get('/')
        print(resp.context['products_list'])
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('products_list' in resp.context)
        self.assertTrue(product in resp.context['products_list'])

    def test_get_absolute_url(self):
        product = Product.objects.get(id=1)
        self.assertEqual(product.get_absolute_url(), '/product_detail/tv/')

    def test_the_existence_of_the_product(self):
        product = Product.objects.get(id=1)
        resp = self.client.get(product.get_absolute_url())
        self.assertEqual(product.name, resp.context["product"].name)


    # def test_product_name(self):
    #     product = Product.objects.get(id=1)
    #     field_label = product._meta.get_field('name').verbose_name
    #     self.assertEqual(field_label, 'name')




#создание продуктов и оьратиться на глвнцю страницу и проверить существуют ли он
#тест на полную статью выводит ли нам товар
#сделать запрос в корзину правлиьно ли нас редеректит, проверить если ли товары в корзине,
#тесты создают тестовую базу (нужно в setup методе создавать записи)
#обязательно наполнить тестовую базу инфой методом setup