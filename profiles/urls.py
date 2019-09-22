from django.urls import path
from .views import *


urlpatterns = [
    path("<int:pk>/", ProfileDetail.as_view(), name='profile'),
    path("edit/<int:pk>", ProfileUpdate.as_view(), name="edit_profile"),
]