from django.db import models

from basedata.models import ciudades, versiones_norma, formularios_saq
 


# modelo de la tabla clientes
class clientes(models.Model):

    id_cliente = models.AutoField(primary_key=True)
    razon_social = models.CharField(max_length=150)
    identificacion = models.CharField(max_length=15)
    nombre_comercial = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    telefono = models.CharField(max_length=15)
    telefono2 = models.CharField(null=True,max_length=15, default='')
    codigo_postal = models.CharField(max_length=150)
    
    #llave foranea para la tabla ciudad
    ciudad = models.ForeignKey(ciudades, on_delete=models.CASCADE)
    
    tipo_cliente = models.CharField(max_length=16)
    nivel = models.CharField(max_length=1)
    estado_cliente = models.CharField(max_length=15)
    
    def __str__(self):
        return self.id_cliente
    
    
# modelo de la tabla contactos de los clientes
class contactos(models.Model):

    id_contacto = models.AutoField(primary_key=True)
    nombre_contacto = models.CharField('nombre_contacto', max_length=100)
    cargo_contacto = models.CharField('cargo_contacto', max_length=50)
    email_contacto = models.CharField('email_contacto', max_length=100)
    cliente = models.ForeignKey(clientes, on_delete=models.CASCADE)
    estado_contacto = models.CharField(max_length=15)


# modelo de la tabla certificados de los clientes
class certificados(models.Model):

    id_certificado = models.AutoField(primary_key=True)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    tipo_cliente = models.CharField(max_length=16 )
    nivel = models.CharField(max_length=1)
    codigo_certificado = models.CharField(max_length=20)
    versiones_norma = models.ForeignKey(versiones_norma, on_delete=models.CASCADE)
    cliente = models.ForeignKey(clientes, on_delete=models.CASCADE, )
    estado_certificado = models.CharField(max_length=15 )
    formularios_saq = models.ForeignKey(formularios_saq, on_delete=models.CASCADE, default=None)



