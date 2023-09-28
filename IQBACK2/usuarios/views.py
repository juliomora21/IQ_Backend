from django.shortcuts import render

from rest_framework.views import APIView
from django.contrib.auth import logout

from rest_framework.response import Response

from django.contrib.auth import login, logout

from rest_framework import status

from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password

from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .usuariosSerializers import UserSerializer


User = get_user_model()


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username = username, password=password)
        if user is None:
            return Response({'success': 'true', 'status': 204, 'mensaje': 'credenciales invalidas', }, status=401)
        
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})


class LogoutView(APIView):
    def post(self, request):
        try:
            # Obtenemos el token del usuario autenticado
            token = request.user.auth_token
            # Borramos el token
            token.delete()
            # Retornamos una respuesta exitosa
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            # Retornamos una respuesta con error
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": str(e)})


class cambiarClave(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        user = request.user
        
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not user.check_password(old_password):
            return Response({'old_password': ['Contraseña actual incorrecta.']}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({'confirm_password': ['Las contraseñas no coinciden.']}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Contraseña actualizada correctamente.'}, status=status.HTTP_200_OK)
