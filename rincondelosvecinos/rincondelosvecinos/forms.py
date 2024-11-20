from django import forms
from .models import Usuario

class UsuarioForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_contrasena = forms.CharField(widget=forms.PasswordInput, label="Confirme Contraseña")

    class Meta:
        model = Usuario
        fields = [
            "rut",
            "nombre",
            "primer_apellido",
            "segundo_apellido",
            "email",
            "contrasena",
            "direccion_particular",
            "direccion_facturacion",
            "telefono",
        ]

    def clean(self):
        cleaned_data = super().clean()
        
        # Extraer los datos del formulario
        rut = cleaned_data.get("rut")
        email = cleaned_data.get("email")
        telefono = cleaned_data.get("telefono")
        contrasena = cleaned_data.get("contrasena")
        confirm_contrasena = cleaned_data.get("confirm_contrasena")

        # Verificar que el RUT no esté registrado
        if Usuario.objects.filter(rut=rut).exists():
            self.add_error("rut", "Este RUT ya está registrado. Por favor, verifica los datos ingresados.")

        # Verificar que el correo no esté registrado
        if Usuario.objects.filter(email=email).exists():
            self.add_error("email", "Este correo electrónico ya está registrado. Por favor, usa otro correo.")

        # Verificar que el teléfono no esté registrado
        if Usuario.objects.filter(telefono=telefono).exists():
            self.add_error("telefono", "Este número de teléfono ya está registrado. Por favor, usa otro número.")

        # Validar coincidencia de contraseñas
        if contrasena and confirm_contrasena and contrasena != confirm_contrasena:
            self.add_error("confirm_contrasena", "Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")

        return cleaned_data