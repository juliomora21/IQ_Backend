from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render
from rest_framework import generics

from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
# Create your views here.

from .models import paises, departamentos, ciudades, versiones_norma, formularios_saq

from .baseSerializer import paisesSerializer, departamentosSerializer, ciudadesSerializer
from .baseSerializer import versionesNormaSerializer, formulariosSaqSerializer



class paisesList(generics.ListCreateAPIView):

    queryset = paises.objects.all()
    serializer_class = paisesSerializer

    def list(self, request, *args, **kwargs):
        # Realizar la consulta en la base de datos
        ciudades = self.get_queryset()

        if not ciudades.exists():
            # Si no hay datos, retorna una respuesta con status 204 y un mensaje
            return Response(
                {   
                    'success': 'true',
                    'status': 204,
                    'mensaje': 'No hay datos de ciudades configuradas',
                }, 
                status=status.HTTP_204_NO_CONTENT
            )
        
        else:
            # Si hay datos, realiza la serialización y retorna la respuesta con los datos
            serializer = self.get_serializer(ciudades, many=True)
            return Response(serializer.data)



class DepartamentosPorPaisAPI(APIView):

    def get(self, request, pais_id):
        # Obtén las ciudades del país especificado
        ListadoDepartamentos = departamentos.objects.filter(pais_id=pais_id)

        # Verificar si no se encontraron ciudades
        if not ListadoDepartamentos.exists():
            # Retornar una respuesta con código de estado 404 (No encontrado)
            return Response(
                {   
                    'success': 'true',
                    'status': 204,
                    'mensaje': 'No se encontraron departamentos  para el país especificado',
                }, 
                status=status.HTTP_204_NO_CONTENT
            )

        # Serializa las ciudades en formato JSON
        serializer = departamentosSerializer(ListadoDepartamentos, many=True)
        
        # Retorna la respuesta con las ciudades serializadas
        #return Response(serializer.data)
        return Response(serializer.data)
    
class DepartamentosPorID(APIView):

    def get(self, request, id_departamento):
        # Obtén las ciudades del país especificado
        ListadoDepartamentos = departamentos.objects.filter(id_departamento=id_departamento)

        # Verificar si no se encontraron ciudades
        if not ListadoDepartamentos.exists():
            # Retornar una respuesta con código de estado 404 (No encontrado)
            return Response(
                {   
                    'success': 'true',
                    'status': 204,
                    'mensaje': 'No se encontraron departamentos  para el país especificado',
                }, 
                status=status.HTTP_204_NO_CONTENT
            )

        # Serializa las ciudades en formato JSON
        serializer = departamentosSerializer(ListadoDepartamentos, many=True)
        
        # Retorna la respuesta con las ciudades serializadas
        #return Response(serializer.data)
        return Response(serializer.data)



class CiudadesPorDepartamentoAPI(APIView):

    def get(self, request, departamento_id):
        # Obtén las ciudades del país especificado
        ListadoCiudades = ciudades.objects.filter(departamento_id=departamento_id)

        # Verificar si no se encontraron ciudades
        if not ListadoCiudades.exists():
            # Retornar una respuesta con código de estado 404 (No encontrado)
            # return Response({'mensaje': 'No se encontraron ciudades para el departamento especificado'}, status=404)
            return Response(
                {   
                    'success': 'true',
                    'status': 204,
                    'mensaje': 'No se encontraron ciudades para el departamento especificado',
                }, 
                status=status.HTTP_204_NO_CONTENT
            )

        # Serializa las ciudades en formato JSON
        serializer = ciudadesSerializer(ListadoCiudades, many=True)
        # Retorna la respuesta con las ciudades serializadas
        # return Response(serializer.data)
        return Response(serializer.data)
    


class CiudadesPorID(APIView):

    def get(self, request, id_ciudad):
        # Obtén las ciudades del país especificado
        ListadoCiudades = ciudades.objects.filter(id_ciudad=id_ciudad)

        # Verificar si no se encontraron ciudades
        if not ListadoCiudades.exists():
            # Retornar una respuesta con código de estado 404 (No encontrado)
            # return Response({'mensaje': 'No se encontraron ciudades para el departamento especificado'}, status=404)
            return Response(
                {   
                    'success': 'true',
                    'status': 204,
                    'mensaje': 'No se encontraron ciudades para el departamento especificado',
                }, 
                status=status.HTTP_204_NO_CONTENT
            )

        # Serializa las ciudades en formato JSON
        serializer = ciudadesSerializer(ListadoCiudades, many=True)
        # Retorna la respuesta con las ciudades serializadas
        # return Response(serializer.data)
        return Response(serializer.data)
    


class VersionesNormasList(generics.ListCreateAPIView):
    queryset = versiones_norma.objects.all()
    serializer_class = versionesNormaSerializer

    def list(self, request, *args, **kwargs):
        # Realizar la consulta en la base de datos
        versiones_normas = self.get_queryset()

        if not versiones_normas.exists():
            # Si no hay datos, retorna una respuesta con status 204 y un mensaje
            return Response(
                {   
                    'success': 'true',
                    'status': 204,
                    'mensaje': 'No hay datos de versiones configuradas',
                }, 
                status=status.HTTP_204_NO_CONTENT)
        else:
            # Si hay datos, realiza la serialización y retorna la respuesta con los datos
            serializer = self.get_serializer(versiones_normas, many=True)
            # return Response(serializer.data)
            return Response(serializer.data)

class formulariosSAQList(generics.ListCreateAPIView):
    
    def list(self, request, tipo_cliente):
        
        # Realizar la consulta en la base de datos
        listado_formularios = formularios_saq.objects.filter(estado_formulario_saq='activo', tipo_cliente = tipo_cliente )

        if not listado_formularios.exists():
            # Si no hay datos, retorna una respuesta con status 204 y un mensaje
            return Response(
                {   
                    'success': 'true',
                    'status': 204,
                    'mensaje': 'No hay datos de Formularios SAQ configurados',
                }, 
                status=status.HTTP_204_NO_CONTENT)
        else:
            # Si hay datos, realiza la serialización y retorna la respuesta con los datos
            serializer = formulariosSaqSerializer(listado_formularios, many=True)
            
            # return Response(serializer.data)
            return Response(serializer.data)
