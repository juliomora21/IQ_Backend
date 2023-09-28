from rest_framework import serializers

from .models import paises, departamentos, ciudades, versiones_norma, formularios_saq

class paisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = paises
        fields = ('id_pais','pais',)

class departamentosSerializer(serializers.ModelSerializer):
    class Meta:
        model = departamentos
        fields = ('id_departamento', 'departamento', 'pais_id')

class ciudadesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ciudades
        fields = ('id_ciudad', 'ciudad', 'departamento_id')

class versionesNormaSerializer(serializers.ModelSerializer):
    class Meta:
        model = versiones_norma
        fields = ('id_version_norma', 'version_norma', 'estado_version_norma')

class formulariosSaqSerializer(serializers.ModelSerializer):
    class Meta:
        model = formularios_saq
        fields = ('id_formulario_saq', 'formulario_saq', 'estado_formulario_saq', 'tipo_cliente')