document.querySelector('.custom-form').addEventListener('submit', function (event) {
    event.preventDefault(); // Evitar el envío inmediato del formulario

    const form = event.target;
    const carrito = JSON.parse(localStorage.getItem('cart')) || []; // Obtener carrito de localStorage

    // Enviar carrito al servidor para sincronizarlo
    fetch('/sincronizar-carrito/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}',
        },
        body: JSON.stringify({ carrito: carrito }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Si la sincronización fue exitosa, proceder con el inicio de sesión
            form.submit();
        } else {
            alert('Error al sincronizar el carrito. Intenta nuevamente.');
        }
    })
    .catch(error => console.error('Error al sincronizar el carrito:', error));
});