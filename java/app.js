var Nombre = document.getElementById("Nombre");
var Apellido = document.getElementById("Apellido");
var Rut = document.getElementById("Rut");
var Correo = document.getElementById("Correo");
var Contraseña = document.getElementById("contraseña");
var error = document.getElementById("error");
error.style.color = 'red';

function Registrarse(){
    console.log('Registrandose...');

    var mensajesError = [];

    if(Nombre.value === null || Nombre.value === ''){
        mensajesError.push("ingrese su nombre ");
    }else if (Nombre.value.lenght < 3 || Nombre.value.lenght > 22){
        mensajesError.push("el nombre debe tener entre 3 y 22 caracteres");
    }    
    if(Rut.value === null || Rut.value === ''){
        mensajesError.push("ingrese su rut ");
    }else if (Rut.value.lenght < 9 || Rut.value.lenght > 10){
        mensajesError.push("el nombre debe tener entre 9 y 10 caracteres");
    }
    if(Apellido.value === null || Apellido.value === ''){
        mensajesError.push('ingresa tu apellido');
    }else if (Apellido.value.length < 3 || Apellido.value.length > 20){
        mensajesError.push("el apellido tiene que tener entre 3 y 22 caracteres");
    }
    if(Correo.value === null || Correo.value === ''){
        mensajesError.push('ingresa tu email');
    }
    if(Contraseña.value === null ||Contraseña.value === ''){
        mensajesError.push("ingrese una contraseña");
    }else if(Contraseña.value.lenght < 4 || Contraseña.value.lenght > 22 ){
        mensajesError.push("la contraseña debe tener entre 4 y 22 caracteres");
    }
}
