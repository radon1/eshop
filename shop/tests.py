from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Product, Category, Cart, CartItem


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user_1 = User.objects.create_user(username='Bob', password='Marli')
        user_1.save()
        category = Category.objects.create(name='category', slug='category')
        # Cart.objects.create(user=user_1, accepted='False')
        pr = Product.objects.create(name='TV', category=category, slug='tv',
                               description='Описание', price='29999', quantity='50',
                               color='black', availability='True', detailed_description='Детальное описание',
                               rank='5', discount='10')
        CartItem.objects.create(product=pr, cart=Cart.objects.get(user=user_1, accepted='False'))

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

    def test_cart(self):
        cart = Cart.objects.get(id=1)
        self.assertEqual(cart.user.username, 'Bob')

    def test_cart_page(self):
        resp = self.client.get('/cart/')
        self.assertRedirects(resp, '/accounts/login/?next=/cart/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='Bob', password='Marli')
        resp = self.client.get('/cart/')
        self.assertEqual(str(resp.context['user']), 'Bob')
        self.assertEqual(resp.status_code, 200)

    def test_items_in_cart(self):
        cart_item = CartItem.objects.get(id=1)
        # cart_product = CartItem.objects.get(product_id=1)
        login = self.client.login(username='Bob', password='Marli')
        resp = self.client.get('/cart/')
        print(resp.context["object_list"])
        self.assertTrue(cart_item in resp.context["object_list"])

    # def test_cart_product(self):
    #     cart_item = CartItem.objects.create(username=)

#создание продуктов и оьратиться на глвнцю страницу и проверить существуют ли он
#тест на полную статью выводит ли нам товар
#сделать запрос в корзину правлиьно ли нас редеректит, проверить если ли товары в корзине,
#тесты создают тестовую базу (нужно в setup методе создавать записи)
#обязательно наполнить тестовую базу инфой методом setup