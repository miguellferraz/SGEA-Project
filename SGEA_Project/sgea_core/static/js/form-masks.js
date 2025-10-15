// sgea_core/static/js/form-masks.js

document.addEventListener('DOMContentLoaded', function () {

    // Lógica da Máscara de Telefone
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

    // Lógica do Autocomplete do Login
    const usernameInput = document.querySelector('input[name="username"]');
    const passwordInput = document.querySelector('input[name="password"]');
    if (usernameInput) {
        usernameInput.setAttribute('autocomplete', 'username');
    }
    if (passwordInput) {
        passwordInput.setAttribute('autocomplete', 'current-password');
    }

    // --- LÓGICA CORRIGIDA DO MENU HAMBURGUER ---
    const menuBtn = document.getElementById('menu-btn');
    const menu = document.getElementById('menu');

    if (menuBtn && menu) {
        menuBtn.addEventListener('click', () => {
            menu.classList.toggle('hidden');
        });
    }
});