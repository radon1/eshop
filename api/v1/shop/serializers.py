from rest_framework import serializers
from shop.models import Product, Category, CartItem, Cart, Order

from photologue.models import Gallery, Photo


class PhotoSerializer(serializers.ModelSerializer):
    image = serializers.URLField(read_only=True, source='image.url')

    class Meta:
        model = Photo
        fields = ['image']


class GallerySerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Gallery
        fields = ['photos']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'image', 'price', 'availability']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    gallery = GallerySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ['slug']


class CreateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"] #"cart", "product",


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'price_sum']


class OrderListView(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['date', 'total', 'accepted']

