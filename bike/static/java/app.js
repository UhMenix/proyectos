var Nombre = document.getElementById("Nombre");
var Apellido = document.getElementById("Apellido");
var Rut = document.getElementById("Rut");
var Correo = document.getElementById("Correo");
var Contraseña = document.getElementById("Contraseña");  
var error = document.getElementById("error");
error.style.color = 'red';

function Registrarse() {
    console.log('Registrandose...');

    var mensajesError = [];

    if (Nombre.value === null || Nombre.value === '') {
        mensajesError.push("Ingrese su nombre");
    } else if (Nombre.value.length < 3 || Nombre.value.length > 22) {  
        mensajesError.push("El nombre debe tener entre 3 y 22 caracteres");
    }

    if (Rut.value === null || Rut.value === '') {
        mensajesError.push("Ingrese su RUT");
    } else if (Rut.value.length < 9 || Rut.value.length > 10) {  
        mensajesError.push("El RUT debe tener entre 9 y 10 caracteres");
    }

    if (Apellido.value === null || Apellido.value === '') {
        mensajesError.push("Ingresa tu apellido");
    } else if (Apellido.value.length < 3 || Apellido.value.length > 22) {  
        mensajesError.push("El apellido tiene que tener entre 3 y 22 caracteres");
    }

    if (Correo.value === null || Correo.value === '') {
        mensajesError.push("Ingresa tu email");
    }

    if (Contraseña.value === null || Contraseña.value === '') {
        mensajesError.push("Ingrese una contraseña");
    } else if (Contraseña.value.length < 4 || Contraseña.value.length > 22) {  
        mensajesError.push("La contraseña debe tener entre 4 y 22 caracteres");
    }

    if (mensajesError.length > 0) {
        error.innerHTML = mensajesError.join(', ');
        return false;
    }

    return true;
}
