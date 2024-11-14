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
    
    
# prueba conexión a BD
from django.db import connection

try:
    connection.ensure_connection()  # Esto intenta conectar con la base de datos
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
    