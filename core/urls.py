from django.urls import path
from .views import LeadListCreate, LeadDetail, ClientListCreate, ClientDetail

urlpatterns = [
    path('leads/', LeadListCreate.as_view(), name='lead-list'),  # Mejor nombre
    path('leads/<int:pk>/', LeadDetail.as_view(), name='lead-detail'),  # Ruta para detalle
    path('clients/', ClientListCreate.as_view(), name='client-list'),  # Mejor nombre
    path('clients/<int:pk>/', ClientDetail.as_view(), name='client-detail'),  # Ruta para detalle
]
