from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('security.urls')),
    path('', include('categories.urls')),
    path('', include('recipes.urls')),
    path('', include('contact.urls')),
    path('', include('recetas_helper.urls')),

    #path('', include('home.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
