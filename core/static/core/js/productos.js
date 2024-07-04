$(document).ready(function() {

    // Cambiar el texto del combo de categoría por "Seleccione una categoría"
    var select = document.querySelector('select[name="categoria"]');
    if (select) {
        var defaultOption = select.querySelector('option[value=""]');
        if (defaultOption) {
            defaultOption.text = "Seleccione una categoría";
        }
    }

    // Asignar placeholders para ayudar a los usuarios
    $('#id_nombre').attr('placeholder', 'Ingrese aqui el nombre del juego');
    $('#id_descripcion').attr('placeholder', 'Ingrese aqui una descripción del juego');
    $('#id_precio').attr('placeholder', 'Ingrese precio normal del juego');
    $('#id_descuento_subscriptor').attr('placeholder', 'Ingrese el descuento para subscriptores');
    $('#id_descuento_oferta').attr('placeholder', 'Ingrese el descuento de oferta');

    // Agregar una validación por defecto para que la imagen la exija como campo obligatorio
    $.extend($.validator.messages, {
        required: "Este campo es requerido",
    });

    // Agregar validación para que la suma de los descuentos no supere el 100%
    $.validator.addMethod('sumaDescuentos', function(value, element) {
        
        var descuentoSubscriptor = parseFloat($('#id_descuento_subscriptor').val());
        var descuentoOferta = parseFloat($('#id_descuento_oferta').val());
        var sumaDescuentos = descuentoSubscriptor + descuentoOferta;
        
        if (isNaN(descuentoSubscriptor) || isNaN(descuentoOferta)) return true;

        return sumaDescuentos <= 100;

    }, 'La suma de los descuentos no puede superar el 100%');

    $('#form').validate({ 
        rules: {
            'categoria': {
                required: true,
            },
            'nombre': {
                required: true,
                minlength: 3,
                maxlength: 100,
            },
            'descripcion': {
                required: true,
                minlength: 20,
                maxlength: 800,
            },
            'precio': {
                required: true,
                digits: true,
                number: true,
                min: 0,
            },
            'descuento_subscriptor': {
                required: true,
                digits: true,
                number: true,
                range: [0, 100],
                sumaDescuentos: true,
            },
            'descuento_oferta': {
                required: true,
                digits: true,
                number: true,
                range: [0, 100],
                sumaDescuentos: true,
            },
        },
        messages: {
            'categoria': {
                required: 'Debe ingresar la categoría del producto',
            },
            'nombre': {
                required: 'Debe ingresar el nombre del producto',
                minlength:'El nombre debe tener un minimo de 3 caracteres',
                maxlength:'El nombre debe tener maximo 100 caracteres',
            },
            'descripcion': {
                required: 'Debe ingresar la descripción del producto',
                minlength:'La descripcion debe tener un minimo de 20 caracteres',
                maxlength:'La descripcion debe tener un maximo de 800 caracteres',
            },
            'precio': {
                required: 'Debe ingresar el precio del producto',
                number: 'Debe ingresar un número',
                min: 'El precio debe ser mayor o igual a 0',
                digits: 'Debe ingresar un número entero',
            },
            'descuento_subscriptor': {
                required: 'Debe ingresar el % de descuento para subscriptores',
                number: 'Debe ingresar un número',
                digits: 'Debe ingresar un número entero',
                range: 'El descuento debe ser un número entre 0 y 100',
            },
            'descuento_oferta': {
                required: 'Debe ingresar el % de descuento para ofertas',
                number: 'Debe ingresar un número',
                digits: 'Debe ingresar un número entero',
                range: 'El descuento debe ser un número entre 0 y 100',
            },
        },
        errorPlacement: function(error, element) {
            error.insertAfter(element); // Inserta el mensaje de error después del elemento
            error.addClass('error-message'); // Aplica una clase al mensaje de error
        },
    });

});
