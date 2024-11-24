from django.db import models
from datetime import datetime, timedelta
from django.utils.timezone import now
from django.contrib.auth.hashers import make_password

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
    salt = models.CharField(max_length=16, blank=True, null=True)  # Salt para encriptar contraseñas
    is_active = models.BooleanField(default=False)  # Usuario inactivo hasta confirmar
    bloqueado = models.BooleanField(default=False)  # Indica si la cuenta está bloqueada
    intentos_fallidos = models.IntegerField(default=0)  # Número de intentos fallidos
    fecha_registro = models.DateTimeField(default=now, editable=False)  # Fecha y hora de registro
    # Campos para control de intentos
    last_login = models.DateTimeField(blank=True, null=True)  # Campo para el último inicio de sesión

    USERNAME_FIELD = 'email'  # Define que el email será el identificador único
    REQUIRED_FIELDS = ['rut', 'contrasena']  


    class Meta:
        db_table = 'Usuarios'
    
    def __str__(self):
        return f"{self.nombre} {self.primer_apellido}"
    

    # Métodos requeridos por Django
    @property
    def is_anonymous(self):
        """Si el usuario es anónimo."""
        return False

    @property
    def is_authenticated(self):
        """Si el usuario está autenticado."""
        return True
    
    def get_email_field_name(self):
        return 'email'
    
    def password(self):
        return 'contrasena'
    
    def esta_bloqueado(self):
        """Verificar si el usuario está bloqueado."""
        if self.bloqueado_hasta and datetime.now() < self.bloqueado_hasta:
            return True
        return False


    def reiniciar_intentos(self):
        """Reiniciar los intentos fallidos y desbloquear al usuario."""
        self.intentos_fallidos = 0
        self.bloqueado_hasta = None
        self.save()

class Administrador(models.Model):
    id = models.AutoField(primary_key=True)  
    rut = models.CharField(max_length=12, unique=True)  # RUT único
    email = models.EmailField(max_length=100, unique=True)  # Email único y validado como dirección de correo
    contrasena = models.CharField(max_length=255)  # Contraseña (considera usar hashed passwords en la práctica)

    class Meta:
        db_table = 'Administrador'

    def __str__(self):
        return f"{self.rut} - {self.email}"
    
    def save(self, *args, **kwargs):
       # Encripta la contraseña antes de guardar
        if not self.pk:  # Solo si es una creación, no en una actualización
            self.contrasena = make_password(self.contrasena)
        super().save(*args, **kwargs)

    def crear_admin():
        rut = input("Ingrese el RUT del administrador: ")
        email = input("Ingrese el correo electrónico del administrador: ")
        contrasena = input("Ingrese la contraseña del administrador: ")

    # Crea el objeto Administrador y guarda en la base de datos
        administrador = Administrador(rut=rut, email=email, contrasena=contrasena)
        administrador.save()  # Esto automáticamente encriptará la contraseña por el método save()
        print(f"Administrador creado: {administrador}")

    if __name__ == "__main__":
        crear_admin()
    


# prueba conexión a BD
from django.db import connection

try:
    connection.ensure_connection()  # Esto intenta conectar con la base de datos
    print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")



    