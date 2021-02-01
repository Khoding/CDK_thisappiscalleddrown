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
        tippy('.popover-btn', {
            content(reference) {
                const id = reference.getAttribute('data-template');
                const template = document.getElementById(id);
                return template.innerHTML;
            },
            allowHTML: true,
            theme: 'koolapic',
            trigger: 'click',
            animation: 'pop'
        });

        tippy('.tooltip-btn', {
            content(reference) {
                const id = reference.getAttribute('data-template');
                const template = document.getElementById(id);
                return template.innerHTML;
            },
            onShow(instance) {
                setTimeout(() => {
                    instance.hide();
                }, 2000);
            },
            allowHTML: true,
            theme: 'koolapic',
            trigger: 'mouseenter focus',
            hideOnClick: false,
            animation: 'pop'
        });
    }
});