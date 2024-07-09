document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Evita que el formulario se envíe automáticamente

        // Obtener los valores de los campos del formulario
        const username = document.getElementById('username').value.trim();
        const password = document.getElementById('password').value.trim();

        // Validar que los campos no estén vacíos
        if (username === '' || password === '') {
            alert('Por favor, complete todos los campos.');
            return;
        }

        // Redirigir a la página principal
        window.location.href = 'bike/index.html'; 
    });
});
