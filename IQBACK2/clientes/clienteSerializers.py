from rest_framework import serializers
from .models import clientes, contactos, certificados
from basedata.baseSerializer import formulariosSaqSerializer, versionesNormaSerializer

class clienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = clientes
        fields = (
            'id_cliente',
            'razon_social',
            'identificacion',
            'nombre_comercial',
            'direccion',
            'telefono',
            'telefono2',
            'codigo_postal',
            'tipo_cliente',
            'nivel',
            'estado_cliente',
            'ciudad_id'
        )


class ContactoClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = contactos
        fields = ('id_contacto', 'nombre_contacto', 'cargo_contacto',
                  'email_contacto', 'cliente_id', 'estado_contacto')


class certificadosSerializer(serializers.ModelSerializer):

    class Meta:
        model = certificados
        fields = (
            'id_certificado',
            'fecha_emision',
            'fecha_vencimiento',
            'estado_certificado',
            'cliente_id',
            'versiones_norma_id',
            'nivel',
            'tipo_cliente',
            'codigo_certificado', 
            'formularios_saq_id'
        )


class certificadosClientesSerializer(serializers.ModelSerializer):
    
    cliente = clienteSerializer()
    versiones_norma = versionesNormaSerializer()
    formularios_saq = formulariosSaqSerializer()

    class Meta:
        model = certificados
        fields = '__all__'
