from functools import wraps
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from jose import jwt
from django.conf import settings
import time









def logueado(redirect_url=None):
    def metodo(func):
        @wraps(func)
        def _decorator(request, *args, **kwargs):
            req = args[0]
            if not req.headers.get('Authorization') or req.headers.get('Authorization') == None:
                return Response({"error":"No autorizado"}, status=HTTP_401_UNAUTHORIZED)
            header = req.headers.get('Authorization').split('')
            try:
                resuelto = jwt.decode(header[1], settings.SECRET_KEY, algorithms=['HS512'])
            except Exception as e:
                return Response({"error":"No autorizado"}, status=HTTP_401_UNAUTHORIZED)
            if int(resuelto['exp'])>int(time.time()):
                return func(request, args, **kwargs)
            else:
                return Response({"error":"No autorizado"}, status=HTTP_401_UNAUTHORIZED)
            
        return _decorator
    return metodo
    


