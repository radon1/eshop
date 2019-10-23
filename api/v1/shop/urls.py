from django.urls import path, include
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.ViewSetProductDetail)

urlpatterns = [
    path("p/", include(router.urls)),
    path('categories/', views.Categories.as_view()),
    path('cart_items/', views.CartItemsView.as_view()),
    path('cart_items/<int:pk>/', views.CartItemsView.as_view()),
    path('prod/<int:pk>/', views.GenericProductDetail.as_view()),
    path('<int:pk>/', views.ProductDetail.as_view()),
    path('cart_update/<int:pk>/', views.CartItemUpdate.as_view()),
    path('cart_delete/<int:pk>/', views.CartItemDelete.as_view()),
    path('add_order/', views.AddOrderView.as_view()),
    path('order_list/', views.OrderListView.as_view()),
    path('', views.ProductList.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
