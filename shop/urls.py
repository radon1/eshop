from django.urls import path
from .views import *


urlpatterns = [
    path('', ProductsList.as_view(), name='products'),
    path('product_detail/<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    path("add-cart-item/<slug:slug>/<int:pk>/", AddCartItem.as_view(), name="add_cartitem"),
    path("cart/", CartItemList.as_view(), name="cart_item"),
    path("edit/<int:pk>/", EditCartItem.as_view(), name="edit_item"),
    path("delete/<int:pk>/", RemoveCartItem.as_view(), name="del_item"),
    path("add_order/", AddOrder.as_view(), name="add_order"),
    path("order_list/", OrderList.as_view(), name="order_list"),
    path("category/<slug:slug>", CategoryProduct.as_view(), name='category'),
    path('sort/', SortProducts.as_view(), name='sort'),
    path('checkout/<int:pk>/', CheckOut.as_view(), name='checkout'),
    path('test/', Test.as_view(), name='test'),
]
