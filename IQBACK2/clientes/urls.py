from django.urls import path

from .views import ClienteCreateView, ListadoClientesView, ClienteUpdateView, ClientePorNombreList, ClientePorID
from .views import ContactoCreateView, ContactoUpdateView, ContactoListado
from .views import certificadoCreateView, certificadoListado, certificadoUpdateView, generarCertificadoPDF, DescargarPDFView, consultarCertificado


urlpatterns = [
    path('createCliente/',ClienteCreateView.as_view(), name = 'cliente-create'),
    path('listadoClientes/',ListadoClientesView.as_view(), name = 'cliente_list'),
    path('updateCliente/<int:id_cliente>/',ClienteUpdateView.as_view(), name = 'cliente-update'),
    path('ListadoClienteRazonSocial/<str:razon_social>/',ClientePorNombreList.as_view(), name = 'cliente-list'),
    path('ListadoClienteID/<int:id_cliente>/',ClientePorID.as_view(), name = 'cliente-list'),

    path('createContactoCliente/',ContactoCreateView.as_view(), name = 'contacto-cliente-create'),
    path('updateContactoCliente/<int:id_contacto>/',ContactoUpdateView.as_view(), name = 'contacto-update'),
    path('listadoContactoCliente/<int:cliente_id>/',ContactoListado.as_view(), name = 'contacto-list'),

    path('createCertificadoCliente/',certificadoCreateView.as_view(), name = 'certificado-cliente-create'),
    path('listadoCertificadoCliente/<int:cliente_id>/',certificadoListado.as_view(), name = 'certificados-list'),
    path('updateCertificadoCliente/<int:id_certificado>/',certificadoUpdateView.as_view(), name = 'contacto-update'),
    path('generarCertificadoPDF/',generarCertificadoPDF.as_view(), name = 'certificado-cliente-generar'),
    path('descargarPDF/<str:codigo>',DescargarPDFView.as_view(), name = 'descargar_pdf'),
    path('consultarCertificado/<str:codigo>',consultarCertificado.as_view(), name = 'descargar_pdf'),
]