from django.urls import path
from .views import RegisterListAPIView, VerificationListAPIView, LoginListAPIView





urlpatterns = [
    path('seguridad/registro', RegisterListAPIView.as_view()),
    path('seguridad/verificacion/<str:token>', VerificationListAPIView.as_view()),
    path('seguridad/login', LoginListAPIView.as_view()),
    
]