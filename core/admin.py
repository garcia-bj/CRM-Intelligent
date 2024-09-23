from django.contrib import admin
from .models import Usuario, Cliente, Lead, Interaccion, Venta, AutomatedTask

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'rol', 'fecha_creacion')
    search_fields = ('nombre', 'email', 'rol')
    list_filter = ('rol', 'fecha_creacion')
    date_hierarchy = 'fecha_creacion'  # Añadida jerarquía de fechas

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'telefono', 'pais', 'direccion', 'fecha_creacion', 'updated_at')
    search_fields = ('nombre', 'email', 'telefono')
    list_filter = ('pais', 'fecha_creacion')
    date_hierarchy = 'fecha_creacion'

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fuente', 'estado', 'vendedor', 'fecha_creacion')
    list_filter = ('estado', 'vendedor')
    search_fields = ('cliente__nombre', 'fuente')
    date_hierarchy = 'fecha_creacion'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('cliente', 'vendedor')  # Optimización de relaciones

@admin.register(Interaccion)
class InteraccionAdmin(admin.ModelAdmin):
    list_display = ('lead', 'tipo', 'fecha')
    search_fields = ('lead__cliente__nombre', 'tipo')
    list_filter = ('tipo', 'fecha')
    date_hierarchy = 'fecha'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('lead', 'lead__cliente')  # Optimización de relaciones

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'vendedor', 'producto', 'cantidad', 'precio', 'fecha')
    search_fields = ('cliente__nombre', 'producto')
    list_filter = ('vendedor', 'fecha')
    date_hierarchy = 'fecha'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('cliente', 'vendedor')  # Optimización de relaciones

@admin.register(AutomatedTask)
class AutomatedTaskAdmin(admin.ModelAdmin):
    list_display = ('lead', 'vendedor', 'tipo', 'fecha_programada', 'completada')
    search_fields = ('lead__cliente__nombre', 'vendedor__nombre', 'tipo')
    list_filter = ('tipo', 'completada', 'fecha_programada')
    date_hierarchy = 'fecha_programada'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('lead', 'vendedor')  # Optimización de relaciones
