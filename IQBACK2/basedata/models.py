from django.db import models

# Create your models here.


class paises(models.Model):
    id_pais = models.AutoField(primary_key=True)
    pais = models.CharField('pais', max_length=200)


class departamentos(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    departamento = models.CharField('departamento', max_length=200)
    pais = models.ForeignKey(paises, on_delete=models.CASCADE)


class ciudades(models.Model):
    id_ciudad = models.AutoField(primary_key=True)
    ciudad = models.CharField('ciudad', max_length=200)
    
    #el campo toma el nombre de departamento_id y genera la llave foranea de tabla departamento 
    departamento = models.ForeignKey(departamentos, on_delete=models.CASCADE)


class versiones_norma(models.Model):
    id_version_norma = models.AutoField(primary_key=True)
    version_norma = models.CharField('version_norma', max_length=200)
    estado_version_norma = models.CharField(max_length=15)

class formularios_saq(models.Model):
    id_formulario_saq = models.AutoField(primary_key=True)
    formulario_saq = models.CharField('formulario_saq', max_length=30)
    estado_formulario_saq = models.CharField(max_length=15)
    tipo_cliente = models.CharField(max_length=16, default='')

