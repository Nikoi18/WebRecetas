from django.urls import path
from .views import RecetasListAPIView, RecetasDetailAPIView

urlpatterns = [
    path('recetas/', RecetasListAPIView.as_view()),
    path('recetas/<int:id>', RecetasDetailAPIView.as_view()),
]