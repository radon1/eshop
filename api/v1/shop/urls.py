from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('', views.ProductList.as_view()),
    path('product/<int:pk>/', views.ProductDetail.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
