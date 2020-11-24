/* Nécessite :
   JQuery (Slim supporté)
   Popper.js
   Tippy.js
 */
$(document).ready(function () {
    /* Fonction utilisée quand la page a fini de charger */
    $(function () {
        createPopovers()
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
});