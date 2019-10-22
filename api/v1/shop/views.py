from rest_framework import permissions, generics, viewsets

from shop.models import Product, Category, Cart, CartItem
from .serializers import ProductSerializer, ProductDetailSerializer, CategorySerializer, CreateCartItemSerializer, CartItemSerializer
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
