$(document).ready(function () {
    $(function () {
        createPopovers()
        createShowPasswordButtons()
    });

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

    function createShowPasswordButtons() {
        let buttons = $('.show-passwd-btn')

        for (let i = 0; i < buttons.length; i++) {
            let button = buttons[i];
            button.addEventListener('click', togglePassword)
        }
    }

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