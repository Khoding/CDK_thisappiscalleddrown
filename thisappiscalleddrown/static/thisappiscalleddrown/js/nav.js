/**
 * Fenêtres modales
 * Nécessite :
 * JQuery (Slim supporté)
 * Anime.js
 * Bootstrap
 */

$(document).ready(function () {
    $(function () {
        initNavTogglerButtons()
    })

    /* Initialise les boutons pour toggler les nav */
    function initNavTogglerButtons() {
        let buttons = $('.nav-toggler')

        for (let i = 0; i < buttons.length; i++) {
            buttons[i].addEventListener('click', toggleNavFromTogglerListener)
            let nav = $(buttons[i].dataset.target)[0]
            let overlay = $(nav.dataset.overlay)[0];
            overlay.addEventListener('click', toggleNavFromOverlayListener)
        }
    }

    /* Event listener pour le clic sur le "navigation toggler" */
    function toggleNavFromTogglerListener(event) {
        let toggler = event.currentTarget
        let nav = $(toggler.dataset.target)[0]
        let overlay = $(nav.dataset.overlay)[0]

        nav.classList.toggle("toggled")
        overlay.classList.toggle("toggled")
    }

    /* Event listener pour le clic sur l'overlay */
    function toggleNavFromOverlayListener(event) {
        let overlay = event.currentTarget
        let nav = $(overlay.dataset.target)[0]

        nav.classList.toggle("toggled")
        overlay.classList.toggle("toggled")
    }
})