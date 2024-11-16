function validateRut(input) {
 input.value = input.value.replace(/[^0-9]/g, '');
 
 if (input.value.length > 8) {
     input.value = input.value.slice(0, 8);
 }
 
 // Validar que el valor sea un número entre 1000000 y 99999999
 const rutNumber = parseInt(input.value);
 if (input.value.length === 8) {
     if (rutNumber < 1000000 || rutNumber > 99999999) {
         input.setCustomValidity('RUT inválido');
         input.style.borderColor = 'red';
     } else {
         input.setCustomValidity('');
         input.style.borderColor = 'green';
     }
 } else {
     input.setCustomValidity('');
     input.style.borderColor = '';
 }
 
 validateForm();
}

function validateForm() {
 const usernameInput = document.querySelector('input[name="username"]');
 const passwordInput = document.querySelector('input[name="password"]');
 const submitButton = document.querySelector('button[type="submit"]');
 
 if (!usernameInput || !passwordInput || !submitButton) return;

 if (usernameInput.value.length === 8 && 
     passwordInput.value.length > 0 && 
     !usernameInput.validity.customError) {
     submitButton.disabled = false;
     submitButton.classList.remove('btn-secondary');
     submitButton.classList.add('btn-primary');
 } else {
     submitButton.disabled = true;
     submitButton.classList.remove('btn-primary');
     submitButton.classList.add('btn-secondary');
 }
}

document.addEventListener('DOMContentLoaded', function() {
 const usernameInput = document.querySelector('input[name="username"]');
 const passwordInput = document.querySelector('input[name="password"]');
 const submitButton = document.querySelector('button[type="submit"]');
 
 if (submitButton) {
     submitButton.classList.add('btn-secondary');
     submitButton.disabled = true;
 }
 
 if (passwordInput) {
     passwordInput.addEventListener('input', validateForm);
 }
 
 validateForm();
});