from rest_framework import generics, serializers  # Descomentar la importación de serializers
from .models import Lead, Cliente, Usuario
from django.core.mail import send_mail
#from .serializers import LeadSerializer

# Serializador para Lead
class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'  # Considera especificar los campos si es necesario
    
    def create(self, validated_data):
        # Obtener la región y los intereses del lead
        region = validated_data.get('region')
        intereses = validated_data.get('intereses', [])
        vendedores_a_notificar = []  # Lista para almacenar vendedores asignados
        
        # Lógica de asignación de vendedor basada en región e intereses
        vendedor_asignado = None
        
        # Primero tratamos de asignar por región
        if region:
            vendedor_asignado = Usuario.objects.filter(rol='vendedor', region=region).first()

        # Asignación por intereses si no se encontró vendedor por región
        if not vendedor_asignado and intereses:
            vendedores_por_interes = Usuario.objects.filter(rol='vendedor', intereses__in=intereses).distinct()
            vendedor_asignado = vendedores_por_interes.first()  # Se asigna el primer vendedor por intereses
            vendedores_a_notificar = list(vendedores_por_interes)  # Se agregan todos los vendedores relacionados a la lista

        # Asignar el vendedor al lead
        validated_data['vendedor'] = vendedor_asignado
        
         # Crear el lead con la asignación
        lead = super().create(validated_data)

        # Enviar correos de notificación a los vendedores asignados
        if vendedores_a_notificar:
            for vendedor in vendedores_a_notificar:
                send_mail(
                    'Nuevo Lead Asignado',
                    f'Se te ha asignado un nuevo lead: {lead.cliente.nombre}',
                    'correoprueba@gmail.com',  # Correo desde el que se envía
                    [vendedor.email],  # Enviar al correo del vendedor
                    fail_silently=False,
                )

        return lead
# Vista para listar y crear Leads
class LeadListCreate(generics.ListCreateAPIView):
    queryset = Lead.objects.select_related('vendedor').all()  # Mejora la consulta
    serializer_class = LeadSerializer

# Vista para obtener, actualizar y eliminar un Lead
class LeadDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

# Serializador para Cliente
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'  # Considera especificar los campos si es necesario

    def validate_telefono(self, value):  # Validación opcional para el número de teléfono
        if not value.isdigit():
            raise serializers.ValidationError("El teléfono solo puede contener números.")
        return value
