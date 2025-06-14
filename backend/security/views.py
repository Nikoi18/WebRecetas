from django.shortcuts import render 
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework import status 
from django.contrib.auth.models import User 
from .models import UsersMetadata 
import uuid 
import os
from utilities import utilities 
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth import authenticate 
from jose import jwt 
from django.conf import settings 
from datetime import datetime, timedelta 
import time



 




# Create your views here.

class RegisterListAPIView(APIView):
    
    def post(self, request):
        if request.data.get('name')== None or not request.data.get('name'):
            return Response({'error': 'El nombre es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('email')== None or not request.data.get('email'):
            return Response({'error': 'El correo es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('password')== None or not request.data.get('password'):
            return Response({'error': 'El password es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=request.data['email']).exists():
            return Response({'error': 'El correo ya existe'}, status=status.HTTP_400_BAD_REQUEST)
        

        token = uuid.uuid4()
        # Para la prueba: usa un valor por defecto para BASE_URL y asegura una barra separadora.
        url = f"{os.getenv('BASE_URL','http://127.0.0.1:8000/')}/seguridad/verificacion/{token}"
        try:
            user = User.objects.create_user(username=request.data['email'],  password=request.data['password'], email=request.data['email'], first_name=request.data['name'], last_name='', is_active=0)
            UsersMetadata.objects.create(token=token, user_id=user.pk)
            html= f"""
            <h1>Verificacion de cuenta - WebRecetas</h1>
            <p>Hola {request.data['name']} te haz registrado exitosamente. Para activar tu cuenta haz click en el siguiente enlace</p>
            <a href="{url}"> aqui </a>
            <br/>
            o copia y pega la siguiente URL en tu navegador.
            <br/>
            {url}                    
            <p>Gracias.</p>
            """
            utilities.send_mail(html, 'Verificacion de cuenta', request.data['email'])

        except Exception as e:
            return Response({'error': 'ocurrio un error al crear el usuario'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'ok': 'usuario creado exitosamente'}, status=status.HTTP_201_CREATED)
    
class VerificationListAPIView(APIView):
    
    def get(self, request, token):
        if token == None or not token:
            return Response({'error': 'El token es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            data=UsersMetadata.objects.filter(token=token).filter(user__is_active=0).get()

            UsersMetadata.objects.filter(token=token).update(token="")

            User.objects.filter(id=data.user_id).update(is_active=1)

            return HttpResponseRedirect(os.getenv('BASE_URL','http://127.0.0.1:5173/login'))
        except UsersMetadata.DoesNotExist:
           raise Http404
        
class LoginListAPIView(APIView):

    def post(self, request):

        if request.data.get('email')== None or not request.data.get('email'):
            return Response({'error': 'El correo es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('password')== None or not request.data.get('password'):
            return Response({'error': 'El password es requerido'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.filter(email=request.data['email']).get()
        
        except User.DoesNotExist:
            return Response({'error': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)
        
        auth = authenticate(request, username=request.data.get('email'), password=request.data.get('password'))

        if auth is not None:
            date = datetime.now()
            after = date + timedelta(days=1)
            date_number = int(datetime.timestamp(after))
            payload = {"id":user.pk, "ISS":os.getenv("BASE_URL","http://127.0.0.1:8000/"), "iat":int(time.time()), "exp":int(date_number)}
            try:
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS512')
                return Response({'id':user.pk, 'name':user.first_name, 'token':token})
            except Exception as e:
                return Response({'error': 'inesperado'}, status=status.HTTP_400_BAD_REQUEST)
            
            
        else:
            return Response({'error': 'Credenciales invalidas'}, status=status.HTTP_401_UNAUTHORIZED)



        