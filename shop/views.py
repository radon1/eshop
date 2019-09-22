from django.conf import settings
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum, Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.base import View
from .models import (Product, Cart, CartItem, Order, Category)
from .forms import CartItemForm
from profiles.forms import ProfileForm
from profiles.models import Profile


class ProductsList(ListView):
    """Список всех продуктов"""
    model = Product
    template_name = "shop/list_product.html"
    paginate_by = 5
    context_object_name = 'products_list'
    queryset = Product.objects.order_by('-id')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        return context


class ProductDetail(DetailView):
    """Карточка товара"""
    model = Product
    context_object_name = 'product'
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CartItemForm()
        return context


class CartItemList(ListView):
    """Товары в корзине пользователя"""
    template_name = 'shop/cart.html'
    cart_items = ''

    def get_queryset(self):
        self.cart_items = CartItem.objects.filter(cart__user=self.request.user, cart__accepted=False)
        return self.cart_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cart_id"] = Cart.objects.get(user=self.request.user, accepted=False).id
        context["total"] = self.cart_items.aggregate(Sum('price_sum'))
        return context


# class AddCartItem(CreateView, UpdateView):
#     model = CartItem
#     form_class = CartItemForm
#     template_name = 'shop/add_cart_item.html'
#     success_url = ''
#
#     def form_valid(self, form):
#         messages.add_message(self.request, settings.MY_INFO, "Товар добавлен")
#         form.instance.cart = Cart.objects.get(user=self.request.user)
#         form.instance.product_id = self.kwargs.get("pk")
#         form.save()
#         self.success_url = "/product_detail/{}/".format(self.kwargs.get("slug"))
#         return super().form_valid(form)
#
#     def get_object(self, queryset=None):
#         try:
#             return CartItem.objects.get(cart__user=self.request.user, product_id=self.kwargs.get("pk"), cart__accepted=False)
#         except:
#             pass


class AddCartItem(View):
    """Добавление товара в корзину"""
    def post(self, request, slug, pk):
        quantity = request.POST.get("quantity", None)
        if quantity is not None and int(quantity) > 0:
            try:
                item = CartItem.objects.get(
                    cart__user=request.user,
                    product_id=pk,
                    cart__accepted=False)
                item.quantity += int(quantity)
            except CartItem.DoesNotExist:
                item = CartItem(
                    cart=Cart.objects.get(user=request.user, accepted=False),
                    product_id=pk,
                    quantity=int(quantity)
                )
            item.save()
            messages.add_message(request, settings.MY_INFO, "Товар добавлен")
            return redirect("/product_detail/{}/".format(slug))
        else:
            messages.add_message(request, '80', "Значение не может быть 0")
            return redirect("/product_detail/{}/".format(slug))


class EditCartItem(View):
    '''Редактирование товара в корзине'''
    def post(self, request, pk):
        quantity = request.POST.get("quantity", None)
        if quantity:
            item = CartItem.objects.get(id=pk, cart__user=request.user)
            item.quantity = int(quantity)
            item.save()
        return redirect("cart_item")


class RemoveCartItem(View):
    '''Удаление товара из корзины'''
    def get(self, request, pk):
        CartItem.objects.get(id=pk, cart__user=request.user).delete()
        messages.add_message(request, settings.MY_INFO, 'Товар удален')
        return redirect("cart_item")


class AddOrder(View):
    """Создание заказа"""
    def post(self, request):
        cart = Cart.objects.get(id=request.POST.get("pk"), user=request.user)
        cart.accepted = True
        cart.save()
        Order.objects.create(cart=cart)
        Cart.objects.create(user=request.user)
        return redirect('order_list')


class OrderList(ListView):
    """Список заказов пользователя"""
    template_name = "shop/order_list.html"
    order = ''

    def get_queryset(self):
        self.order = Order.objects.filter(cart__user=self.request.user, accepted=False)
        return self.order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total"] = self.order.aggregate(Sum('cart__cartitem__price_sum'))
        return context

    def post(self, request):
        """Удаление заказа"""
        order = Order.objects.get(id=request.POST.get("pk"), cart__user=request.user, accepted=False)
        Cart.objects.get(order__id=order.id, user=request.user, accepted=True).delete()
        order.delete()
        return redirect("order_list")


class Search(View):
    """Поиск товаров"""
    def get(self, request):
        search = request.GET.get("search", None)
        products = Product.objects.filter(Q(name__icontains=search) |
                                          Q(category__name__icontains=search))

        paginator = Paginator(products, 5)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        context = {"object_list": products, "page_obj": page_obj}

        return render(request, "shop/list_product.html", context)


class CheckOut(View):
    """Оплата заказа"""
    def get(self, request, pk):
        order = Order.objects.filter(
            id=pk,
            cart__user=request.user,
            accepted=False
        ).aggregate(Sum('cart__cartitem__price_sum'))
        form = ProfileForm(instance=Profile.objects.get(user=request.user))
        return render(request, 'shop/checkout.html', {"order": order, "form": form})


class CategoryProduct(ListView):
    """Список товаров из категории"""
    template_name = "shop/list_product.html"
    paginate_by = 5
    context_object_name = 'products_list'

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        node = Category.objects.get(slug=slug)
        if Product.objects.filter(category__slug=slug).exists():
            products = Product.objects.filter(category__slug=slug)
        else:
            products = Product.objects.filter(category__slug__in=[x.slug for x in node.get_family()])
        return products.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all()
        return context



class SortProducts(View):
    """Фильтр товаров"""

    def post(self, request):
        category = request.POST.get("category", None)
        price_1 = request.POST.get("price1", 1)
        price_2 = request.POST.get("price2", 1000000000)
        availability = request.POST.get("availability", None)
        print(price_1)
        print(price_2)
        print(availability)

        filt = []

        if category:
            cat = Q()
            cat &= Q(category__name__icontains=category)
            filt.append(cat)
        if price_1 or price_2:
            price = Q()
            price &= Q(price__gte=int(price_1)) & Q(price__lte=int(price_2))
            filt.append(price)
        if availability:
            if availability == "False":
                avail = False
            elif availability == "True":
                avail = True
            else:
                avail = True
            availability = Q()
            availability &= Q(availability=avail)
            filt.append(availability)

        sort = Product.objects.filter(*filt)

        return render(request, "shop/list_product.html", {"products_list": sort})


class Test(View):
    '''Test Render'''
    def get(self, request):
        return render(request, 'shop/test.html')