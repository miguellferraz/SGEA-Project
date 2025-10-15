document.addEventListener('DOMContentLoaded', function () {
    const phoneInput = document.getElementById('id_telefone');

    if (phoneInput) {
        phoneInput.addEventListener('input', function (e) {
            let value = e.target.value.replace(/\D/g, '');
            value = value.substring(0, 11);

            if (value.length > 2) {
                value = `(${value.substring(0, 2)}) ${value.substring(2)}`;
            }
            if (value.length > 10) {
                value = `${value.substring(0, 10)}-${value.substring(10)}`;
            }
            e.target.value = value;
        });
    }
});

const usernameInput = document.querySelector('input[name="username"]');
const passwordInput = document.querySelector('input[name="password"]');

if (usernameInput) {
    usernameInput.setAttribute('autocomplete', 'username');
}
if (passwordInput) {
    passwordInput.setAttribute('autocomplete', 'current-password');
}