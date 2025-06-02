from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category
from .serializers import CategorySerializer
from http import HTTPStatus
from rest_framework.exceptions import NotFound, bad_request
from django.http import Http404
from django.utils.text import slugify



class CategoriesListAPIView(APIView):

    
    def get(self, request):
        data = Category.objects.order_by('-id').all()
        datos_jason = CategorySerializer(data, many= True)
        return Response(datos_jason.data, status=HTTPStatus.OK)
    

    def post(self, request):  
        if request.data.get("name") == None:
            return Response ({"estado":"error","mensaje":"El campo name es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        try:
            Category.objects.create(name=request.data["name"])
            return Response({"estado":"ok", "mensaje":"Categoria creada correctamente"}, status=HTTPStatus.CREATED)
        except Exception as e:
            raise Http404
    
    
class CategoriesDetailAPIView(APIView):


    def get(self, request, id):
        try:
            data = Category.objects.get(pk=id)
            return Response({"data":{"id":data.pk, "name":data.name, "slug":data.slug}}, status=HTTPStatus.OK)
        except Category.DoesNotExist:
            raise NotFound(detail="Id no encontrado")
    
    
    def put(self, request, id):
        if request.data.get("name") == None:
            return Response ({"Estado":"Error", "Mensaje":"El campo name es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        if not request.data.get("name"):
            return Response ({"Estado":"Error", "Mensaje":"El campo name es obligatorio"}, status=HTTPStatus.BAD_REQUEST)
        try:
            data = Category.objects.filter(pk=id).get()
            Category.objects.filter(pk=id).update(name=request.data.get("name"), slug=slugify(request.data.get("name")))
            return Response({"estado":"ok", "mensaje":"Categoria actualizada correctamente"}, status=HTTPStatus.OK)
        except Category.DoesNotExist:
            raise NotFound(detail="Id no encontrado")


    def delete(self, request, id):
        try:
            data = Category.objects.filter(pk=id).get()
            Category.objects.filter(pk=id).delete()
            return Response({"estado":"ok", "mensaje":"Categoria eliminada correctamente"}, status=HTTPStatus.OK)
        except Category.DoesNotExist:
            raise Http404
             



    
    