from django.urls import path
# from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('categories/', views.Categories.as_view()),
    path('<int:pk>/', views.ProductDetail.as_view()),
    path('', views.ProductList.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns)
