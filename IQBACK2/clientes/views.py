
from rest_framework import generics

from basedata.baseSerializer import formulariosSaqSerializer, versionesNormaSerializer

from .models import clientes, contactos, certificados
from basedata.models import ciudades, formularios_saq, versiones_norma

from .clienteSerializers import clienteSerializer, ContactoClienteSerializer
from .clienteSerializers import certificadosClientesSerializer, certificadosSerializer

from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status


import pythoncom
from docx2pdf import convert
from docx import Document
import os

from django.http import FileResponse






# ------------------------------ CLIENTES -------------------------------

class ClienteCreateView(generics.CreateAPIView):
    serializer_class = clienteSerializer
    serializer_clientes = clienteSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            ciudad_id = request.data.get('ciudad_id')
            identificacion = request.data.get('identificacion')

            # -------------- Validar si la ciudad existe --------------------------------------
            try:
                ciudad = ciudades.objects.get(id_ciudad=ciudad_id)
            except ciudades.DoesNotExist:
                # return Response({'error': 'La ciudad no existe'}, status=404)
                return Response(
                    {
                        'success': 'true',
                        'status': 204,
                        'mensaje': 'Error en la configuracion basica del sistema. La ciudad no existe',
                    },
                    status=status.HTTP_204_NO_CONTENT
                )

            # -------------- Valida si el cliente ya existe en la base de datos ----------------
            try:
                cliente_existente = clientes.objects.get(
                    identificacion=identificacion)
                # Si el cliente ya existe, puedes mostrar un mensaje de error o redirigir a otra página
                # return Response({'mensaje': 'El cliente ya existe en la base de datos.'}, status=404)
                return Response(
                    {
                        'success': 'true',
                        'status': 204,
                        'mensaje': 'El cliente ya existe en el sistema.',
                    },
                    status=status.HTTP_204_NO_CONTENT
                )

            except clientes.DoesNotExist:

                

                if ('telefono2' in request.data):
                    telefono2 = request.data.get('telefono2')
                else:
                    telefono2 = ''

                # Si el cliente no existe, puedes crear uno nuevo y guardarlo en la base de datos
                nuevo_cliente = clientes(
                    razon_social=request.data.get('razon_social'),
                    identificacion=request.data.get('identificacion'),
                    nombre_comercial=request.data.get('nombre_comercial'),
                    direccion=request.data.get('direccion'),
                    telefono=request.data.get('telefono'),
                    telefono2=telefono2,
                    codigo_postal=request.data.get('codigo_postal'),
                    tipo_cliente=request.data.get('tipo_cliente'),
                    nivel=request.data.get('nivel'),
                    estado_cliente=request.data.get('estado_cliente'),
                    ciudad_id=request.data.get('ciudad_id')
                )

                # Guarda el nuevo cliente en la base de datos
                nuevo_cliente.save()


                # retornar mensaje con estatus 201
                return Response({ "id_cliente": nuevo_cliente.id_cliente}, status=201)

            else:
                # Renderiza el formulario para ingresar los datos del cliente
                # return Response({'mensaje': 'El cliente no se pudo crear, intentalo nuevamente'}, status=401)
                return Response(
                    {
                        'success': 'true',
                        'status': 204,
                        'mensaje': 'El cliente no se pudo crear, intentalo nuevamente.',
                    },
                    status=status.HTTP_204_NO_CONTENT
                )

        else:
            # Si los campos no son válidos, retornar una respuesta de error
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListadoClientesView(generics.ListCreateAPIView):
    queryset = clientes.objects.all()
    serializer_class = clienteSerializer

    def list(self, request, *args, **kwargs):

        # Realizar la consulta en la base de datos
        listClientes = self.get_queryset()

        if not listClientes.exists():
            # Si no hay datos, retorna una respuesta con status 204 y un mensaje
            return Response({},status=status.HTTP_200_OK)

        else:
            # Si hay datos, realiza la serialización y retorna la respuesta con los datos
            serializer = self.get_serializer(listClientes, many=True)
            return Response(serializer.data)


class ClienteUpdateView(generics.RetrieveUpdateAPIView):
    queryset = clientes.objects.all()
    serializer_class = clienteSerializer
    lookup_field = 'id_cliente'  # Campo utilizado para filtrar el objeto cliente

    def put(self, request, *args, **kwargs):
        
        
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.ciudad_id = request.data['ciudad_id']
        
        serializer = self.get_serializer(instance, data = request.data, partial = partial)

        serializer.is_valid(raise_exception = True)
        self.perform_update(serializer)
        

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.put(request, *args, **kwargs)


class ClientePorNombreList(generics.ListAPIView):
    
    def get(self, request, razon_social):

        # Obtén las ciudades del país especificado
        ListadoClientes = clientes.objects.filter(
            razon_social__icontains=razon_social)

        # Verificar si no se encontraron ciudades
        if not ListadoClientes.exists():
            # Retornar una respuesta con código de estado 404 (No encontrado)
            # return Response({'mensaje': 'No se encontraron ciudades para el departamento especificado'}, status=404)
            return Response({},status=status.HTTP_204_NO_CONTENT)

        # Serializa las ciudades en formato JSON
        serializer = clienteSerializer(ListadoClientes, many=True)
        # Retorna la respuesta con las ciudades serializadas
        # return Response(serializer.data)
        return Response(serializer.data)
    

class ClientePorID(generics.ListAPIView):
    
    def get(self, request, id_cliente):
        
        # Obtén las ciudades del país especificado
        ListadoClientes = clientes.objects.filter(id_cliente = id_cliente)

        # Verificar si no se encontraron ciudades
        if not ListadoClientes.exists():
            # Retornar una respuesta con código de estado 404 (No encontrado)
            # return Response({'mensaje': 'No se encontraron ciudades para el departamento especificado'}, status=404)
            return Response(
                {
                    'success': 'true',
                    'status': 204,
                    'mensaje': 'No se encontraron clientes',
                },
                status=status.HTTP_204_NO_CONTENT
            )

        # Serializa las ciudades en formato JSON
        serializer = clienteSerializer(ListadoClientes, many=True)
        # Retorna la respuesta con las ciudades serializadas
        # return Response(serializer.data)
        
        #return Response( {
        #                'success': 'true',
        #                'status': 201,
        #                'mensaje': 'Busqueda correcta',
        #                'document': serializer.data})

        return Response(serializer.data)


# ------------------------------ CONTACTOS -------------------------------

class ContactoCreateView(generics.CreateAPIView):

    serializer_class = ContactoClienteSerializer
    serializer_contactos = ContactoClienteSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():

            post_idCliente = request.data.get('id_cliente')
            post_nombreContacto = request.data.get('nombre_contacto')
            post_email = request.data.get('email_contacto')

            # -------------- Validar si la ciudad existe --------------------------------------
            try:
                cliente = clientes.objects.get(id_cliente=post_idCliente)

            except clientes.DoesNotExist:
                # return Response({'error': 'La ciudad no existe'}, status=404)
                return Response(
                    {
                        'success': 'true',
                        'status': 204,
                        'mensaje': 'Error en la busqueda del cliente.',
                    },
                    status=status.HTTP_204_NO_CONTENT
                )

            # -------------- Valida si el cliente ya existe en la base de datos ----------------
            try:
                contacto_existente = contactos.objects.get(
                    nombre_contacto=post_nombreContacto, email_contacto=post_email)
                # Si el cliente ya existe, puedes mostrar un mensaje de error o redirigir a otra página
                # return Response({'mensaje': 'El cliente ya existe en la base de datos.'}, status=404)
                return Response(
                    {
                        'success': 'true',
                        'status': 204,
                        'mensaje': 'El contacto ya se encuentra registrado en el sistema.',
                    },
                    status=status.HTTP_204_NO_CONTENT
                )

            except contactos.DoesNotExist:

                # Si el cliente no existe, puedes crear uno nuevo y guardarlo en la base de datos
                nuevo_contacto = contactos(
                    nombre_contacto=post_nombreContacto,
                    cargo_contacto=request.data.get('cargo_contacto'),
                    email_contacto=post_email,
                    estado_contacto=request.data.get('estado_contacto'),
                    cliente_id=post_idCliente
                )

                # Guarda el nuevo cliente en la base de datos
                nuevo_contacto.save()

                # retornar mensaje con estatus 201
                return Response({'success': 'true', 'mensaje': 'Contacto creado exitosamente'}, status=201)

            else:
                # Renderiza el formulario para ingresar los datos del cliente
                # return Response({'mensaje': 'El cliente no se pudo crear, intentalo nuevamente'}, status=401)
                return Response(
                    {
                        'success': 'true',
                        'status': 204,
                        'mensaje': 'El contacto no se pudo crear, intentalo nuevamente.',
                    },
                    status=status.HTTP_204_NO_CONTENT
                )

        else:
            # Si los campos no son válidos, retornar una respuesta de error
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ContactoUpdateView(generics.RetrieveUpdateAPIView):
    queryset = contactos.objects.all()
    serializer_class = ContactoClienteSerializer
    lookup_field = 'id_contacto'  # Campo utilizado para filtrar el objeto cliente

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.put(request, *args, **kwargs)


class ContactoListado(APIView):

    def get(self, request, cliente_id):
        
        # Obtén las ciudades del país especificado
        ListadoContactos = contactos.objects.filter(cliente_id=cliente_id)

        # Verificar si no se encontraron ciudades
        if not ListadoContactos.exists():
            # Retornar una respuesta con código de estado 404 (No encontrado)
            # return Response({'mensaje': 'No se encontraron ciudades para el departamento especificado'}, status=404)
            return Response(
                {
                    'success': 'true',
                    'status': 204,
                    'mensaje': 'No se encontraron contactos registrados para el cliente especificado',
                },
                status=status.HTTP_204_NO_CONTENT
            )

        # Serializa las ciudades en formato JSON
        serializer = ContactoClienteSerializer(ListadoContactos, many=True)
        # Retorna la respuesta con las ciudades serializadas
        # return Response(serializer.data)
        return Response(serializer.data)


# ------------------------------ CERTIFICADOS -------------------------------

class certificadoCreateView(generics.CreateAPIView):

    serializer_class = certificadosSerializer
    serializer_certificados = certificadosSerializer

    def post(self, request, *args, **kwargs):

        
        serializer = self.get_serializer(data = request.data)
        
        if serializer.is_valid():

            post_idCliente = request.data.get('cliente_id')
            post_idVersionNorma = request.data.get('versiones_norma_id')
            
            # -------------- Validar si el cliente existe --------------------------------------
            try:

                cliente = clientes.objects.get(id_cliente = post_idCliente)

            except clientes.DoesNotExist:
                
                return Response(
                    {
                        'success': 'true',
                        'status': 204,
                        'mensaje': 'Error en la busqueda del cliente.',
                    },
                    status=status.HTTP_204_NO_CONTENT
                )
            
            # -------------- Validar si la version de la norma existe --------------------------------------
            try:
                versiones = versiones_norma.objects.get(id_version_norma = post_idVersionNorma)

            except versiones_norma.DoesNotExist:
                
                return Response(
                    {
                        'success': 'true',
                        'status': 204,
                        'mensaje': 'Error en la busqueda de la version de la norma.',
                    },
                    status=status.HTTP_204_NO_CONTENT
                )        


            # -------------- Validar si hay certificados --------------------------------------
            try: 
                estado = 'activo'
                resultCert = certificados.objects.get(
                    cliente_id = post_idCliente,
                    versiones_norma_id = post_idVersionNorma,
                    estado_certificado = estado
                )

                return Response(
                    {
                        'success': 'true',
                        'status': 400,
                        'mensaje': 'Se encuentra un certificado vigente para este cliente.',
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            except certificados.DoesNotExist:
                
                nuevo_certificado = certificados(
                    fecha_emision = request.data.get('fecha_emision'),
                    fecha_vencimiento = request.data.get('fecha_vencimiento'),
                    tipo_cliente = request.data.get('tipo_cliente'),
                    nivel = request.data.get('nivel'),
                    cliente_id = post_idCliente,
                    versiones_norma_id = post_idVersionNorma,
                    estado_certificado = request.data.get('estado_certificado'),
                    codigo_certificado = request.data.get('codigo_certificado'),
                    formularios_saq_id = request.data.get('formularios_saq_id')
                )

                # Guarda el nuevo certificado en la base de datos
                nuevo_certificado.save()

                # retornar mensaje con estatus 201
                return Response({'success': 'true', 'mensaje': 'Certificado creado exitosamente'}, status=201)

            except certificados.MultipleObjectsReturned:
                # Renderiza el formulario para ingresar los datos del certificado
                return Response(
                    {
                        'success': 'true',
                        'status': 400,
                        'mensaje': 'Se encuentra un certificado vigente para este cliente.',
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            


        else:
            # Si los campos no son válidos, retornar una respuesta de error
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class certificadoListado(APIView):
    
    def get(self, request, cliente_id):
       
        ListadoCertificados = certificados.objects.filter(cliente_id = cliente_id)

        
        if not ListadoCertificados.exists():
            # Retornar una respuesta con código de estado 404 (No encontrado)
           
            return Response(
                {
                    'success': 'true',
                    'status': 204,
                    'mensaje': 'No se encontraron certificados registrados para el cliente especificado',
                },
                status=status.HTTP_204_NO_CONTENT
            )

        # serializer = certificadosSerializer(ListadoCertificados, many=True)
        serializer = certificadosClientesSerializer(ListadoCertificados, many=True)
        
        
        return Response( serializer.data)
    
class certificadoUpdateView(generics.RetrieveUpdateAPIView):
    
    queryset = certificados.objects.all()
    serializer_class = certificadosSerializer
    lookup_field = 'id_certificado'  # Campo utilizado para filtrar el objeto cliente

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.put(request, *args, **kwargs)

class generarCertificadoPDF(generics.CreateAPIView):
    
    def post(self, request, *args, **kwargs):

        file_path = ''
        ruta_file = 'clientes/report/'
        if (request.data['nivel'] == '1'):
            # Ruta del archivo Word dentro del proyecto
            file_path = 'certificadonivel1.docx'
        elif(request.data['nivel'] == '2'):
            file_path = 'certificadonivel2.docx'
        elif(request.data['nivel'] == '3'):
            file_path = 'certificadonivel3.docx'
        elif(request.data['nivel'] == '4'):
            file_path = 'certificadonivel4.docx'
        
        
        if (file_path != ''):

            
            resultSQLCliente = clientes.objects.filter(id_cliente = request.data['cliente_id']).first()
            if resultSQLCliente is not None:
                
                serializer = clienteSerializer(resultSQLCliente)
                ClienteInfo = serializer.data

                

                resultSQLFormulario = formularios_saq.objects.filter(id_formulario_saq = request.data['formularios_saq_id']).first()
                if resultSQLFormulario is not None:
                    serializer2 = formulariosSaqSerializer(resultSQLFormulario)
                    FormularioInfo = serializer2.data
                    
                    resultVersionNorma = versiones_norma.objects.filter(id_version_norma = request.data['versiones_norma_id']).first()
                    if resultVersionNorma is not None:
                        
                        serializer3 = versionesNormaSerializer(resultVersionNorma)
                        NormaInfo = serializer3.data

                        # Abrir el archivo Word utilizando python-docx
                        doc = Document(ruta_file + file_path)
                        # Palabras a buscar y reemplazar
                        
                        word_replacements = [
                            ('|razon_social|', ClienteInfo['razon_social'].upper()),
                            ('|nivel|', request.data['nivel']),
                            ('|tipo_cliente|', request.data['tipo_cliente'].upper()),
                            ('|version_norma|', NormaInfo['version_norma'].upper()),
                            ('|fecha_emision|', request.data['fecha_emision'].upper()),
                            ('|fecha_expiracion|', request.data['fecha_vencimiento'].upper()),
                            ('|codigo_certificado|', request.data['codigo_certificado'].upper()),
                            ('|formulario_saq|', FormularioInfo['formulario_saq'].upper()),
                            ('|identificacion|', ClienteInfo['identificacion'].upper()),
                            ('|nombre_comercial|', ClienteInfo['nombre_comercial'].upper()),
                            ('|direccion|', ClienteInfo['direccion'].upper()),
                            ('|telefono|', ClienteInfo['telefono'].upper()),
                            ('|telefono2|', ClienteInfo['telefono2'].upper()),
                            ('|codigo_postal|', ClienteInfo['codigo_postal'].upper()),
                        ]
                        

                        for paragraph in doc.paragraphs:
                            for word_to_replace, replacement_word in word_replacements:
                                if paragraph.runs:
                                    if word_to_replace in paragraph.text:

                                        # Guardar el formato de fuente original
                                        original_font_size = paragraph.runs[0].font.size
                                        original_font_name = paragraph.runs[0].font.name

                                        # Reemplazar el texto del título
                                        new_text = paragraph.text.replace(word_to_replace, replacement_word)
                                        paragraph.text = new_text

                                        # Cambiar el tamaño de fuente del título
                                        for run in paragraph.runs:
                                            run.font.size = original_font_size
                                            run.font.name = original_font_name
                        

                        # Guardar el archivo Word modificado
                        modified_file_path = ruta_file + request.data['codigo_certificado'] + '.docx'
                        doc.save(modified_file_path)
                        
                        
                        pythoncom.CoInitialize()
                        convert(modified_file_path)
                        
                        if os.path.exists(modified_file_path):
                            os.remove(modified_file_path)


                        return Response(
                            {
                                'success': 'true',
                                'status': 200,
                                'mensaje': 'No se encontro informacion del Formulario SAQ.',
                            }, 
                            status=status.HTTP_200_OK
                        )
                        
                    
                    else: 
                        return Response(
                            {
                                'success': 'true',
                                'status': 400,
                                'mensaje': 'No se encontro informacion del Formulario SAQ.',
                            }, 
                            status=status.HTTP_400_BAD_REQUEST
                        )

                else: 
                    return Response(
                        {
                            'success': 'true',
                            'status': 400,
                            'mensaje': 'No se encontro informacion del Formulario SAQ.',
                        }, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

            else: 
                return Response(
                    {
                        'success': 'true',
                        'status': 400,
                        'mensaje': 'No se encontro informacion del cliente cliente.',
                    }, 
                    status=status.HTTP_400_BAD_REQUEST
                )

class DescargarPDFView(APIView):
    def get(self, request, codigo):

        ruta_file = 'clientes/report/'

        # Lógica para obtener el archivo PDF
        file_path = ruta_file + codigo + '.pdf'  # Reemplaza esto con la ruta real de tu archivo PDF
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    
class consultarCertificado(APIView):
    
    def get(self, request, codigo):
        
        ListadoCertificados = certificados.objects.filter(codigo_certificado = codigo)

        
        if not ListadoCertificados.exists():
            # Retornar una respuesta con código de estado 404 (No encontrado)
           
            return Response(
                {},
                status=status.HTTP_200_OK
            )

        # serializer = certificadosSerializer(ListadoCertificados, many=True)
        serializer = certificadosClientesSerializer(ListadoCertificados, many=True)
        
        return Response( serializer.data)