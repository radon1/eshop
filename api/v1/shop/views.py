from rest_framework import permissions, generics, viewsets

from shop.models import Product, Category, Cart, CartItem, Order
from .serializers import ProductSerializer, ProductDetailSerializer, CategorySerializer, CreateCartItemSerializer, CartItemSerializer, OrderListView
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response


class ProductList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, pk):
        products = Product.objects.filter(id=pk)
        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        quantity = request.data.get("quantity")
        serializer = CreateCartItemSerializer(data=quantity)
        if serializer.is_valid():
            serializer.save(cart=Cart.objects.get(user=request.user, accepted=False), product_id=pk)
        return Response(status=201)


class Categories(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CartItemsView(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def perform_create(self, serializer):
        serializer.save(cart=Cart.objects.get(user=self.request.user, accepted=False), product_id=self.kwargs.get("pk"))


class GenericProductDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class ViewSetProductDetail(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class CartItemUpdate(generics.UpdateAPIView):
    '''Update товаров в корзине'''
    permission_classes = [permissions.IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CreateCartItemSerializer


class CartItemDelete(generics.DestroyAPIView):
    '''Удаление товара из корзины'''
    permission_classes = [permissions.IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CreateCartItemSerializer


class AddOrderView(APIView):
    '''Создание заказа'''
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        cart = Cart.objects.get(id=request.data.get("pk"), user=request.user)
        if CartItem.objects.filter(cart=cart).exists():
            cart.accepted = True
            cart.save()
            Order.objects.create(cart=cart)
            Cart.objects.create(user=request.user)
        return Response(status=201)


class OrderListView(generics.ListAPIView):
    '''Список заказов пользователя'''
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderListView

    def get_queryset(self):
        pass