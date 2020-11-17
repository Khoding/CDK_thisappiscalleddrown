$(document).ready(function () {
    /* Fonction utilisée quand la page a fini de chargée */
    $(function () {
        createPopovers()
        createShowPasswordButtons()
    });

    /* Crée un popover pour chaque bouton qui en a besoin */
    function createPopovers() {
        let buttons = $('.tooltip-btn')

        for (let i = 0; i < buttons.length; i++) {
            let button = buttons[i];

            let tooltip = $('#' + button.dataset.tooltipId)
            let buttonSelector = '#' + button.id
            tippy(buttonSelector, {
                content: tooltip[0].innerHTML,
                allowHTML: true,
                trigger: 'click',
                theme: 'koolapic'
            })
            tooltip.remove();
        }
    }

    /* Crée un bouton "Montrer le mot de passe" pour chaque input qui en a besoin */
    function createShowPasswordButtons() {
        let buttons = $('.show-passwd-btn')

        for (let i = 0; i < buttons.length; i++) {
            let button = buttons[i];
            button.addEventListener('click', togglePassword)
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