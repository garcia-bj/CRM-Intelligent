from django.db import models

# Tabla de Usuarios (vendedores o administradores)
class Usuario(models.Model):
    ROLES = [
        ('vendedor', 'Vendedor'),
        ('administrador', 'Administrador'),
    ]
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=50, choices=ROLES)
    region = models.CharField(max_length=100, null=True, blank=True)  # Si los vendedores tienen una región asignada
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

# Tabla de Clientes
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    pais = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Este campo se actualizará cada vez que el cliente se modifique

    def __str__(self):
        return self.nombre

# Tabla de Leads
class Lead(models.Model):
    ESTADOS = [
        ('nuevo', 'Nuevo'),
        ('en_proceso', 'En Proceso'),
        ('cerrado', 'Cerrado'),
        ('perdido', 'Perdido'),
    ]
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)  # Permite que el cliente se elimine pero los leads queden con cliente a NULL
    fuente = models.CharField(max_length=100)  # Fuente del lead, por ejemplo, "web", "referencia", etc.
    estado = models.CharField(max_length=50, choices=ESTADOS)
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)  # Los leads deben desaparecer si el vendedor se elimina
    fecha_creacion = models.DateTimeField(auto_now_add=True)

# Nuevos campos para la asignación automática
    region = models.CharField(max_length=100, null=True, blank=True)
    intereses = models.ManyToManyField('Interes', blank=True)  # Puede tener múltiples intereses
    
    def __str__(self):
        return f"Lead para {self.cliente.nombre if self.cliente else 'Cliente eliminado'}"

# Tabla de Interacciones
class Interaccion(models.Model):
    TIPOS_INTERACCION = [
        ('llamada', 'Llamada'),
        ('email', 'Email'),
        ('reunion', 'Reunión'),
    ]
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=TIPOS_INTERACCION)
    descripcion = models.TextField()
    fecha = models.DateTimeField()

    def __str__(self):
        return f"Interacción {self.tipo} para {self.lead.cliente.nombre if self.lead.cliente else 'Cliente eliminado'}"

# Tabla de Ventas
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    vendedor = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField()

    def __str__(self):
        return f"Venta de {self.producto} a {self.cliente.nombre if self.cliente else 'Cliente eliminado'}"

# Tabla de Tareas Automatizadas
class AutomatedTask(models.Model):
    TIPO_TAREA = [
        ('seguimiento', 'Seguimiento de Lead'),
        ('email', 'Envío de Email'),
        ('recordatorio', 'Recordatorio para Vendedor'),
    ]
    lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True)
    vendedor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=TIPO_TAREA)
    fecha_programada = models.DateTimeField()
    completada = models.BooleanField(default=False)

    def __str__(self):
        return f"Tarea {self.tipo} para {self.vendedor.nombre}"
    

# Modelo Interes para relacionar con los Leads
class Interes(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

