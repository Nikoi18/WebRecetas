from rest_framework.views import APIView
from rest_framework.response import Response
from http import HTTPStatus
from rest_framework.exceptions import NotFound
from django.http import Http404
from django.utils.text import slugify
from .models import Recipe
from categories.models import Category
from .serializers import RecipeSerializer
from django.utils.dateformat import DateFormat
from datetime import datetime


class RecetasListAPIView(APIView):
    

    def get(self, request):
        data = Recipe.objects.order_by('-id').all()
        datos_jason = RecipeSerializer(data, many= True)
        return Response(datos_jason.data, status=HTTPStatus.OK)
    

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
        
        try:
            categoria = Category.objects.filter(pk=request.data["category_id"]).get()
        except Category.DoesNotExist:
            return Response({"Error": "La categoría no existe"}, status=HTTPStatus.NOT_FOUND)

    #    if Category.objects.filter(pk=request.data.get("category_id")).exists():
     #       return Response({"Error": "El id ya existe"}, status=HTTPStatus.BAD_REQUEST)
        try:
            Recipe.objects.create(
                name=request.data["name"],
                time=request.data["time"],
                description=request.data["description"],
                category_id=request.data["category_id"],
                date=datetime.now(),
                photo="photo")
            return Response({"estado":"ok", "mensaje":"Receta creada correctamente"}, status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404


class RecetasDetailAPIView(APIView):
    

    def get(self, request, id):
        try:
            data = Recipe.objects.filter(id=id).get()
            return Response({"data":{"id": data.pk, "Nombre": data.name, "Slug": data.slug, "Tiempo": data.time, "Nombre foto": data.photo,"Imagen": f"http://127.0.0.1:8000/media/upload/recipes/{data.photo}", "Descripcion": data.description, "Fecha": DateFormat(data.date).format("d-m-Y"), "Categoria": data.category.name}}, status=HTTPStatus.OK)
        except Recipe.DoesNotExist:
            raise NotFound('Receta no encontrada', HTTPStatus.NOT_FOUND)
        

