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



class HelperListAPIView(APIView):

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
            return Response({"error":"inesperado"},status=status.HTTP_400_BAD_REQUEST)
        
        data = Recipe.objects.filter(user_id=id).order_by('-id').all()
        datos_json=RecipeSerializer(data, many=True)
        return Response({"data":datos_json.data},status=status.HTTP_200_OK)