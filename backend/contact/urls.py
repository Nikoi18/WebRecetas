from django.urls import path
from .views import ContactListAPIView

urlpatterns = [
    path('contacto', ContactListAPIView.as_view())
]