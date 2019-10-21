from rest_framework import permissions

from shop.models import Product
from .serializers import ProductSerializer, ProductDetailSerializer
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
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        products = Product.objects.filter(id=pk)
        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)


class Category(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        products = Product.objects.filter(id=pk)
        serializer = ProductDetailSerializer(products, many=True)
        return Response(serializer.data)
