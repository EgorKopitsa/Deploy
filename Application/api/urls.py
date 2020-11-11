from django.urls import path

from .api_views import *


urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories_list'),
    path('top/', TopListAPIView.as_view(), name='top_list'),
    path('top/<str:id>/', TopDetailAPIView.as_view(), name='top_detail'),
    path('button/', ButtonListAPIView.as_view(), name='button_list'),
    path('button/<str:id>/', ButtonDetailAPIView.as_view(), name='button_detail'),
    path('shoes/', ShoesListAPIView.as_view(), name='shoes_list'),
    path('shoes/<str:id>/', ShoesDetailAPIView.as_view(), name='shoes_detail'),
]
