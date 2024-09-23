from rest_framework import generics, serializers
from .models import Lead, Cliente
from .serializers import LeadSerializer, ClientSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Serializador para Lead
class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'  # Considera especificar los campos si es necesario

    def validate_estado(self, value):
        if value not in ['nuevo', 'en_proceso', 'cerrado', 'perdido']:
            raise serializers.ValidationError("Estado inválido")
        return value

# Serializador para Cliente
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'  # Considera especificar los campos si es necesario

    def validate_telefono(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("El teléfono solo puede contener números.")
        return value

# Vista para listar y crear Leads
class LeadListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.select_related('vendedor').all()  # Mejora la consulta
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]  # Protección con JWT
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['estado', 'vendedor']  # Campos para filtrar
    search_fields = ['cliente__nombre', 'fuente']  # Campos para buscar

# Vista para obtener, actualizar y eliminar un Lead
class LeadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    permission_classes = [IsAuthenticated]  # Protección con JWT

# Vista para listar y crear Clientes
class ClientListCreate(generics.ListCreateAPIView):
    queryset = Cliente.objects.all()  # Cambia 'Client' por 'Cliente'
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]  # Protección con JWT
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['pais']  # Campos para filtrar
    search_fields = ['nombre', 'email', 'telefono']  # Campos para buscar

# Vista para obtener, actualizar y eliminar un Cliente
class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()  # Cambia 'Client' por 'Cliente'
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]  # Protección con JWT
