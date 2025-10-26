from datetime import datetime, timedelta, timezone
import jwt
from django.conf import settings
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Actor

def crear_token(usuario: Actor, dias=7) -> str:
    payload = {
        "id": usuario.id,
        "nombre_usuario": usuario.nombre_usuario,
        "exp": datetime.now(timezone.utc) + timedelta(days=dias),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

class RegisterView(APIView):
    """
    POST /api/register
    body: { nombre_usuario, contrasena }
    201 si ok, 409 si ya existe, 400 si inválido
    """
    def post(self, request):
        nombre = (request.data.get("nombre_usuario") or "").strip()
        password = request.data.get("contrasena") or ""
        if not nombre or len(password) < 6:
            return Response({"error": "Datos inválidos"}, status=400)

        # Hash de contraseña
        hashpw = make_password(password)

        # Como la tabla es 'managed=False', igual podemos insertar usando ORM
        # (Django no gestiona el esquema, pero sí permite CRUD)
        try:
            u = Actor(nombre_usuario=nombre, contrasena=hashpw, creado_en=datetime.now(timezone.utc))
            u.save()
        except IntegrityError:
            return Response({"error": "El usuario ya existe"}, status=409)

        return Response({"ok": True}, status=201)

class LoginView(APIView):
    """
    POST /api/login
    body: { nombre_usuario, contrasena }
    200 -> { token } si ok; 401 si credenciales inválidas
    """
    def post(self, request):
        nombre = (request.data.get("nombre_usuario") or "").strip()
        password = request.data.get("contrasena") or ""
        if not nombre or not password:
            return Response({"error": "Datos inválidos"}, status=400)

        try:
            u = Actor.objects.get(nombre_usuario=nombre)
        except Actor.DoesNotExist:
            return Response({"error": "Credenciales inválidas"}, status=401)

        if not check_password(password, u.contrasena):
            return Response({"error": "Credenciales inválidas"}, status=401)

        token = crear_token(u)
        return Response({"token": token}, status=200)

class MeView(APIView):
    """
    GET /api/me
    headers: Authorization: Bearer <token>
    200 -> { nombre_usuario }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        u: Actor = request.user  # lo puso JWTUsuarioAuthentication
        return Response({"nombre_usuario": u.nombre_usuario}, status=200)
