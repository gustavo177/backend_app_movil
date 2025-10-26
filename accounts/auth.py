from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.conf import settings
import jwt
from .models import Actor

class JWTUsuarioAuthentication(BaseAuthentication):
    """
    Lee 'Authorization: Bearer <token>', valida JWT y carga Usuario en request.user.
    """
    def authenticate(self, request):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return None  # permite endpoints públicos
        token = auth[7:]
        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Token inválido")

        user_id = payload.get("id")
        if not user_id:
            raise exceptions.AuthenticationFailed("Token inválido")

        try:
            u = Actor.objects.get(id=user_id)
        except Actor.DoesNotExist:
            raise exceptions.AuthenticationFailed("No autorizado")

        # DRF espera (user, auth); 'auth' puede ir None
        return (u, None)
