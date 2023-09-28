from django.urls import path
from .views import paisesList, DepartamentosPorPaisAPI, CiudadesPorDepartamentoAPI, DepartamentosPorID, CiudadesPorID
from .views import VersionesNormasList, formulariosSAQList

urlpatterns = [
    path('pais/',paisesList.as_view(), name = 'pais_list'),
    path('api/departamentos/<int:pais_id>', DepartamentosPorPaisAPI.as_view(), name='departamentos_por_pais_api'),
    path('api/departamentos/ID/<int:id_departamento>', DepartamentosPorID.as_view(), name='departamentos_por_ID'),
    path('api/ciudades/<int:departamento_id>', CiudadesPorDepartamentoAPI.as_view(), name='ciudades_por_departamento_api'),
    path('api/ciudades/ID/<int:id_ciudad>', CiudadesPorID.as_view(), name='ciudades_por_ID'),
    path('versiones_norma/',VersionesNormasList.as_view(), name = 'versiones_norma_list'),
    path('api/formularios_saq/<str:tipo_cliente>/',formulariosSAQList.as_view(), name = 'formularios_saq_list'),
]