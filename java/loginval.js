var username = document.getElementById("username");
var correo = document.getElementById("correo");
var password = document.getElementById("password");
var rut = document.getElementById("rut");
var error = document.getElementById("error");

function validar() {
    console.log('Validando formulario...');

    var mensajesError = [];

    if (username.value === null || username.value === '') {
        mensajesError.push("Ingrese su nombre");
    } else if (username.value.length < 3 || username.value.length > 20) {
        mensajesError.push("El nombre debe tener entre 3 y 20 caracteres");
    }

    if (correo.value === null || correo.value === '') {
        mensajesError.push("Ingrese su correo electrónico");
    } else if (!/^\S+@\S+\.\S+$/.test(correo.value)) {
        mensajesError.push("Ingrese un correo electrónico válido");
    }

    if (password.value === null || password.value === '') {
        mensajesError.push("Ingrese su contraseña");
    } else if (password.value.length < 4 || password.value.length > 22) {
        mensajesError.push("La contraseña debe tener entre 4 y 22 caracteres");
    }

    if (rut.value === null || rut.value === '') {
        mensajesError.push("Ingrese su Rut");
    } else if (!/^(\d{1,3}(?:\.\d{1,3}){2}-[\dkK])$/.test(rut.value)) {
        mensajesError.push("Ingrese un Rut válido");
    }

    // Mostrar mensajes de error
    if (mensajesError.length > 0) {
        error.innerHTML = mensajesError.join('<br>');
        return false; // Evita que el formulario se envíe si hay errores
    }

    // Si no hay errores, se puede enviar el formulario
    return true;
}
