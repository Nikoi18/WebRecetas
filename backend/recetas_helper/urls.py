from django.urls import path
from .views import HelperDetailAPIView, HelperListAPIView

urlpatterns = [
    path('recetas/editar/foto', HelperListAPIView.as_view()),
    path('recetas-helper/<int:id>', HelperDetailAPIView.as_view()),
]