from rest_framework import serializers
from shop.models import Product, Category, CartItem, Cart

from photologue.models import Gallery


class GallerySerializer(serializers.ModelSerializer):
    # photos = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='name'
    # )

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
