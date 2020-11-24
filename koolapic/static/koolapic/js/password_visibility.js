/* Nécessite :
   JQuery (Slim supporté)
 */
$(document).ready(function () {
    /* Fonction utilisée quand la page a fini de chargée */
    $(function () {
        createShowPasswordButtons()
    });

    /* Crée un bouton "Montrer le mot de passe" pour chaque input qui en a besoin */
    function createShowPasswordButtons() {
        let buttons = $('.show-passwd-btn')

        for (let i = 0; i < buttons.length; i++) {
            buttons[i].addEventListener('click', togglePassword)
        }
    }

    /* Gestionnaire d'événement "Click" des boutons "Montrer le mot de passe" */
    function togglePassword(event) {
        let button = event.currentTarget
        let passwordInput = $('#' + button.dataset.forField)

        if (button.classList.contains('showPassword')) {
            passwordInput.attr('type', 'password')
            button.innerHTML = '<i class="fas fa-eye"></i>'
            button.classList.toggle('showPassword')
        } else {
            passwordInput.attr('type', 'text')
            button.innerHTML = '<i class="fas fa-eye-slash"></i>'
            button.classList.toggle('showPassword')
        }
    }
});