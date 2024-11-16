from django.db import models

class Producto(models.Model):
    # El campo 'id' es la clave primaria (PK) y Django la crea automáticamente, así que no es necesario declararla explícitamente
    # Si deseas personalizarla, puedes hacerlo así:
    img_url = models.CharField(max_length=255)  # URL de la imagen, varchar(255)
    nombre = models.CharField(max_length=100)   # Nombre del producto, varchar(100)
    precio = models.DecimalField(max_digits=10, decimal_places=0)  # Precio del producto, decimal(10,0)
    stock = models.DecimalField(max_digits=10, decimal_places=0)   # Stock disponible, decimal(10,0)
    descripcion = models.CharField(max_length=300)  # Descripción del producto, varchar(300)
    iva = models.DecimalField(max_digits=10, decimal_places=0)     # IVA, decimal(10,0)
    categoria = models.CharField(max_length=50)    # Categoría del producto, varchar(50)
    admin_id = models.IntegerField()               # ID del administrador, entero
    
    class Meta:
        db_table = 'Productos'  # Este es el nombre exacto de la tabla en la base de datos
   
    def __str__(self):
        return self.nombre
    
    def get_promocion(self):
        # Este método devuelve la promoción activa si existe
        return self.promocion_set.filter(estado='activa').first()  # Asegúrate de que el estado de la promoción sea "activa"


class Promocion(models.Model):
    descuento = models.DecimalField(max_digits=10, decimal_places=0)
    preciodescuento = models.DecimalField(max_digits=10, decimal_places=0)
    estado = models.CharField(max_length=10, choices=[('activa', 'inactiva')])
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Promociones'

    def __str__(self):
        return f"Promoción de {self.producto.nombre}"
    

class Usuario(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=50)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True)
    contrasena = models.CharField(max_length=255)
    direccion_particular = models.CharField(max_length=255)
    direccion_facturacion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)


    class Meta:
        db_table = 'Usuarios'
    
    def __str__(self):
        return f"{self.nombre} {self.primer_apellido}"

class Administrador(models.Model):
    id = models.AutoField(primary_key=True)  
    rut = models.CharField(max_length=12, unique=True)  # RUT único
    email = models.EmailField(max_length=100, unique=True)  # Email único y validado como dirección de correo
    contrasena = models.CharField(max_length=255)  # Contraseña (considera usar hashed passwords en la práctica)

    class Meta:
        db_table = 'Administrador'

    def __str__(self):
        return f"{self.rut} - {self.email}"
    

    
# prueba conexión a BD
from django.db import connection

try:
    connection.ensure_connection()  # Esto intenta conectar con la base de datos
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")




    