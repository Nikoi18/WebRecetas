from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.http import Http404
from django.utils.text import slugify
from django.utils.dateformat import DateFormat
from django.core.files.storage import FileSystemStorage
from .models import Recipe
from .serializers import RecipeSerializer
from categories.models import Category
from http import HTTPStatus
import os
from datetime import datetime
from security.decorators import logueado
from  django.conf import settings
from jose import jwt




class RecetasListAPIView(APIView):
    

    def get(self, request):
        data = Recipe.objects.order_by('-id').all()
        datos_jason = RecipeSerializer(data, many= True)
        return Response(datos_jason.data, status=HTTPStatus.OK)
    
    @logueado()
    def post(self, request):
        required_fields ={
            "name":"name",
            "time":"time",
            "photo":"photo",
            "description":"description",
            "category_id":"category_id",}
        for field_key, field_display_name in required_fields.items():
            if request.data.get(field_key) is None:
                return Response({"Error": f"El campo {field_display_name} es obligatorio"}, status=HTTPStatus.BAD_REQUEST) 
            
        if Recipe.objects.filter(name=request.data.get("name")).exists():
            return Response({"Error": f"El nombre {request.data["name"]} ya existe"}, status=HTTPStatus.BAD_REQUEST)
        
        fs = FileSystemStorage()
        try: 
            photo = f"{datetime.timestamp(datetime.now())}{os.path.splitext(str(request.FILES['photo']))[1]}"
        except Exception as e:
            return Response ({"error":"debe adjuntar una foto en el campo file"}, status= HTTPStatus.BAD_REQUEST)
        
        if request.FILES["photo"].content_type == "image/jpeg" or request.FILES["photo"].contecnt_type == "image/png":       
            try:
                fs.save(f"upload/recipes/{photo}", request.FILES['photo'])
                fs.url(request.FILES['photo'])
            except Exception as e:
                return Response ({"error":"al subir archivo"}, status= HTTPStatus.BAD_REQUEST)


            try:
                Category.objects.filter(pk=request.data["category_id"]).get()
            except Category.DoesNotExist:
                return Response({"Error": "La categoría no existe"}, status=HTTPStatus.NOT_FOUND)

            header = request.headers.get('Authorization').split(' ')
            resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms=['HS512'])


            try:
                Recipe.objects.create(
                    name=request.data["name"],
                    time=request.data["time"],
                    description=request.data["description"],
                    category_id=request.data["category_id"],
                    date=datetime.now(),
                    photo=photo, user_id=resuelto['id'])
                return Response({"estado":"ok", "mensaje":"Receta creada correctamente"}, status=HTTPStatus.CREATED)
            
            except Exception as e:
                raise Http404
        return Response ({"error": "el archivo debe ser JPG o PNG"})


class RecetasDetailAPIView(APIView):
    

    def get(self, request, id):
        try:
            data = Recipe.objects.filter(id=id).get()
            return Response({"data":{"id": data.pk, "Nombre": data.name, "Slug": data.slug, "Tiempo": data.time, "Nombre foto": data.photo,"Imagen": f"http://127.0.0.1:8000/media/upload/recipes/{data.photo}", "Descripcion": data.description, "Fecha": DateFormat(data.date).format("d-m-Y"),"user_id": data.user.pk, "user": data.user.first_name ,"Categoria": data.category.name}}, status=HTTPStatus.OK)
        except Recipe.DoesNotExist:
            raise NotFound('Receta no encontrada', HTTPStatus.NOT_FOUND)

    @logueado()   
    def put(self, request, id):
        required_fields ={
            "name":"name",
            "time":"time",
            "description":"description",
            "category_id":"category_id",}
        for field_key, field_display_name in required_fields.items():
            if request.data.get(field_key) is None:
                return Response({"Error": f"El campo {field_display_name} es obligatorio"}, status=HTTPStatus.BAD_REQUEST) 
        try:
            data = Recipe.objects.filter(id=id).get()
        except Recipe.DoesNotExist:
            return Response({"error":"receta no encontrada"}, status=HTTPStatus.NOT_FOUND)
        
        
        try:
            Category.objects.filter(pk=request.data["category_id"]).get()

        except Category.DoesNotExist:
            return Response({"Error": "La categoría no existe"}, status=HTTPStatus.NOT_FOUND)
            
        if Recipe.objects.filter(name=request.data.get("name")).exists():
            return Response({"Error": f"El nombre {request.data["name"]} ya existe"}, status=HTTPStatus.BAD_REQUEST)
        
        try:
            Recipe.objects.filter(id=id).update(name=request.data["name"], time=request.data.get("time"), description=request.data.get("description"), category_id=request.data.get("category_id"))
            return Response({"estado":"ok", "mensaje":"Receta actualizada correctamente"}, status=HTTPStatus.OK)
        except Exception as e:
            return Response({"error":"ocurrior un error inesperado"}, status=HTTPStatus.NOT_FOUND)

    @logueado()     
    def delete(self, request, id):
        try:
            data = Recipe.objects.filter(pk=id).get()
        except Recipe.DoesNotExist:
            return Response({"error":"receta no encontrada"}, status=HTTPStatus.NOT_FOUND)
        
 
        os.remove(f"media/upload/recipes/{data.photo}")
        Recipe.objects.filter(id=id).delete()
        return Response({"estado":"ok", "mensaje":"Receta eliminada correctamente"}, status=HTTPStatus.OK)