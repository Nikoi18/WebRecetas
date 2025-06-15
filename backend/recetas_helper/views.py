from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status 
from django.http import Http404
from security.decorators import logueado
from security.models import User
from recipes.serializers import RecipeSerializer
from recipes.models import Recipe
import os
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.utils.dateformat import DateFormat




class HelperListAPIView(APIView):

    @logueado()
    def post(self, request):
        if request.data.get('id') == None or not request.data.get('id'):
            return Response ({"error":"id es obligatorio"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            existe=Recipe.objects.filter(pk=request.data['id']).get()
            anterior = existe.photo
        except Recipe.DoesNotExist:
            return Response({"error":"receta no encontrada"}, status=status.HTTP_400_BAD_REQUEST)
        
        fs = FileSystemStorage()
        try: 
            photo = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['photo']))[1]}"
        except Exception as e:
            return Response ({"error":"debe adjuntar una foto en el campo file"}, status=status.HTTP_400_BAD_REQUEST)

        if request.FILES["photo"].content_type == "image/jpeg" or request.FILES["photo"].contecnt_type == "image/png":
            try:
                fs.save(f"upload/recipes/{photo}", request.FILES['photo'])
                fs.url(request.FILES['photo'])
            except Exception as e:
                return Response ({"error":"al subir archivo"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                Recipe.objects.filter(pk=request.data['id']).update(photo=photo)
                os.remove(f"media/upload/recipes/{anterior}")
                return Response({"estado":"ok", "mensaje":"Foto actualizada correctamente"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error":"ocurrio un error inesperado"}, status=status.HTTP_400_BAD_REQUEST)
            

        else:
            return Response ({"error":"debe adjuntar una foto en el campo file"}, status=status.HTTP_400_BAD_REQUEST)

class HelperDetailAPIView(APIView):

    @logueado()
    def get(self, request, id):
        try:
            existe = User.objects.filter(pk=id).get()
        except User.DoesNotExist:
            return Response({"error":"inesperado"},status=status.HTTP_404_NOT_FOUND)
        
        data = Recipe.objects.filter(user_id=id).order_by('-id').all()
        datos_json=RecipeSerializer(data, many=True)
        return Response({"data":datos_json.data},status=status.HTTP_200_OK)
    
class HelperSlugAPIView(APIView):
    
    def get(self, request, slug):
        try:
            data = Recipe.objects.filter(slug=slug).get()
            return Response({"data":{"id":data.pk, "name":data.name, "slug":data.slug, "time":data.time, "description":data.description,  "date":DateFormat(data.date).format("d-m-Y"), "photo": data.photo,"Imagen": f"http://127.0.0.1:8000/media/upload/recipes/{data.photo}","user_id": data.user.pk, "user": data.user.first_name }}, status=status.HTTP_200_OK)  
        except Recipe.DoesNotExist:
            return Response({"error":"inesperado"},status=status.HTTP_404_NOT_FOUND)
        
class HelperHomeAPIView(APIView):

    def get(self, request):
        data = Recipe.objects.order_by('-id').all()[:2]
        datos_jason = RecipeSerializer(data, many= True)
        return Response(datos_jason.data, status=status.HTTP_200_OK)
    
class HelperCategoryAPIView(APIView):

    def get(self, request):
        data = Recipe.objects.filter(category_id=request.GET.get("category_id")).filter(name__icontains=request.GET.get('search')).order_by('-id').all()
        datos_jason = RecipeSerializer(data, many= True)
        return Response(datos_jason.data, status=status.HTTP_200_OK)