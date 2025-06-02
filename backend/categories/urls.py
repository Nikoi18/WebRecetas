from django.urls import path
from .views import CategoriesDetailAPIView, CategoriesListAPIView

urlpatterns = [
    path('categories/', CategoriesListAPIView.as_view()),
    path('categories/<int:id>', CategoriesDetailAPIView.as_view()),
]