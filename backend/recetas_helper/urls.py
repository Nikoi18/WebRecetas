from django.urls import path
from .views import HelperDetailAPIView, HelperListAPIView, HelperSlugAPIView, HelperHomeAPIView, HelperCategoryAPIView

urlpatterns = [
    path('recetas/editar/foto', HelperListAPIView.as_view()),
    path('recetas/slug/<str:slug>', HelperSlugAPIView.as_view()),
    path('recetas-home', HelperHomeAPIView.as_view()),
    path('recetas-helper/<int:id>', HelperDetailAPIView.as_view()),
    path('recetas-buscador', HelperCategoryAPIView.as_view()),
]