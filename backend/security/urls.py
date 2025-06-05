from django.urls import path
from .views import RegisterListAPIView

urlpatterns = [
    path('seguridad/registro', RegisterListAPIView.as_view()),
    
]