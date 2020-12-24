/* Nécessite :
   JQuery (Slim supporté)
   Popper.js
   Tippy.js
 */
// import koolapic from  "../css/tippy.scss";

$(document).ready(function () {
    // const template = document.getElementById('id_username_tooltip')
    /* Fonction utilisée quand la page a fini de charger */
    $(function () {
        createPopovers()
    });

    /* Crée un popover pour chaque bouton qui en a besoin */
    function createPopovers() {
        // let buttons = $('.tooltip-btn')
        // for (let i = 0; i < buttons.length; i++) {
        //     let button = buttons[i];
            tippy('.tooltip-btn', {
                content(reference) {
                    const id = reference.getAttribute('data-template');
                    const template = document.getElementById(id);
                    return template.innerHTML;
                },
                allowHTML: true,
                theme: 'koolapic',
                trigger: 'click',
                // html: 'template'
                // onShow(instance) {
                //     instance.popper.hidden = instance.reference.dataset.tippy ? false : true;
                //     instance.setContent(instance.reference.dataset.tippy);
                // }
            });
            // console.log(test)
        }
    // }
});