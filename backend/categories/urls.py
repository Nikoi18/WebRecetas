from django.urls import path
from .views import CategoriesDetailAPIView, CategoriesListAPIView

urlpatterns = [
    path('categorias/', CategoriesListAPIView.as_view()),
    path('categorias/<int:id>', CategoriesDetailAPIView.as_view()),
]