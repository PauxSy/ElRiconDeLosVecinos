function validarRut(rut) {
    // Expresión regular para validar el formato del RUT
    const rutRegex = /^\d{7,8}-[0-9Kk]$/;
    if (!rutRegex.test(rut)) {
        return false; // Formato inválido
    }

    // Separar el cuerpo del dígito verificador
    let [cuerpo, digitoVerificador] = rut.split("-");
    digitoVerificador = digitoVerificador.toUpperCase();

    // Calcular el dígito verificador
    let suma = 0;
    let multiplicador = 2;

    for (let i = cuerpo.length - 1; i >= 0; i--) {
        suma += multiplicador * parseInt(cuerpo[i]);
        multiplicador = multiplicador === 7 ? 2 : multiplicador + 1;
    }

    let resto = suma % 11;
    let dvCalculado = 11 - resto;
    dvCalculado = dvCalculado === 11 ? "0" : dvCalculado === 10 ? "K" : dvCalculado.toString();

    // Comparar el dígito verificador calculado con el ingresado
    return dvCalculado === digitoVerificador;
}


function validarNombreApellido(valor) {
    return /^[a-zA-ZáéíóúÁÉÍÓÚñÑ]{3,}$/.test(valor);
}

function validarCorreo(correo) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(correo);
}

function validarTelefono(telefono) {
    return /^[0-9]{9}$/.test(telefono);
}

function validarPassword(password) {
    // Requiere al menos 6 caracteres, una letra, un número y un carácter especial (cualquier cosa que no sea letra ni número)
    return /^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z\d])[A-Za-z\d\S]{6,}$/.test(password);
}

// Validación en tiempo real de cada campo
document.getElementById("rutCliente").addEventListener("input", function() {
    document.getElementById("errorRut").style.display = validarRut(this.value) ? "none" : "block";
});

document.getElementById("nombreCliente").addEventListener("input", function() {
    document.getElementById("errorNombre").style.display = validarNombreApellido(this.value) ? "none" : "block";
});

document.getElementById("apellido1Cliente").addEventListener("input", function() {
    document.getElementById("errorApellido1").style.display = validarNombreApellido(this.value) ? "none" : "block";
});

document.getElementById("apellido2Cliente").addEventListener("input", function() {
    document.getElementById("errorApellido2").style.display = validarNombreApellido(this.value) ? "none" : "block";
});

document.getElementById("emailCliente").addEventListener("input", function() {
    document.getElementById("errorEmail").style.display = validarCorreo(this.value) ? "none" : "block";
});

document.getElementById("telefonoCliente").addEventListener("input", function() {
    document.getElementById("errorTelefono").style.display = validarTelefono(this.value) ? "none" : "block";
});

document.getElementById("passCliente").addEventListener("input", function() {
    document.getElementById("errorPassword").style.display = validarPassword(this.value) ? "none" : "block";
});

document.getElementById("confirmPassCliente").addEventListener("input", function() {
    const password = document.getElementById("passCliente").value;
    const confirmPassword = this.value;
    document.getElementById("errorConfirmPassword").style.display = (password === confirmPassword) ? "none" : "block";
});

// Función de validación general para evitar el envío si hay errores
document.getElementById("formularioRegistro").addEventListener("submit", function(event) {
    // Revisar todos los campos
    const rutValido = validarRut(document.getElementById("rutCliente").value);
    const nombreValido = validarNombreApellido(document.getElementById("nombreCliente").value);
    const apellido1Valido = validarNombreApellido(document.getElementById("apellido1Cliente").value);
    const apellido2Valido = validarNombreApellido(document.getElementById("apellido2Cliente").value);
    const correoValido = validarCorreo(document.getElementById("emailCliente").value);
    const telefonoValido = validarTelefono(document.getElementById("telefonoCliente").value);
    const passwordValido = validarPassword(document.getElementById("passCliente").value);
    const passwordsCoinciden = document.getElementById("passCliente").value === document.getElementById("confirmPassCliente").value;

    // Si alguno de los campos es inválido, mostrar advertencia y evitar envío
    if (!rutValido || !nombreValido || !apellido1Valido || !apellido2Valido || !correoValido || !telefonoValido || !passwordValido || !passwordsCoinciden) {
        event.preventDefault(); // Evita el envío del formulario
        document.getElementById("warnings").innerText = "Por favor, corrige los errores antes de registrarte.";
        document.getElementById("warnings").style.color = "red";
    }
});


function validarCampoUnico(campo, valor) {
    fetch(`/validar_campo_unico/?campo=${campo}&valor=${valor}`)
        .then(response => response.json())
        .then(data => {
            const mensajeError = document.getElementById(`error${campo.charAt(0).toUpperCase() + campo.slice(1)}`);
            if (data.existe) {
                mensajeError.style.display = "block";
                mensajeError.innerText = data.mensaje;
            } else {
                mensajeError.style.display = "none";
            }
        })
        .catch(error => console.error("Error en la validación:", error));
}

// Escuchar eventos de entrada para cada campo único
document.getElementById("rutCliente").addEventListener("input", function() {
    validarCampoUnico("rut", this.value);
});

document.getElementById("emailCliente").addEventListener("input", function() {
    validarCampoUnico("email", this.value);
});

document.getElementById("telefonoCliente").addEventListener("input", function() {
    validarCampoUnico("telefono", this.value);
});