/**
 * Fenêtres modales
 * Nécessite :
 * JQuery (Slim supporté)
 * Anime.js
 * Bootstrap
 */

import anime from '../../vendor/node_modules/animejs/lib/anime.es.js';

let modalShow = anime({
    targets: '.modal',
    easing: 'easeOutElastic(1, .5)',
    translateY: '2vh',
    duration: 500,
    opacity: 1,
    autoplay: false
})

let modalHide = anime({
    targets: '.modal',
    easing: 'easeOutElastic(1, .5)',
    translateY: '-2vh',
    duration: 500,
    opacity: 0,
    autoplay: false
})

$(document).ready(function () {
    $(function () {
        let modals = $(".modal")

        for (let i = 0; i < modals.length; i++) {
            modals[i].addEventListener('show.bs.modal', modalShow);
            modals[i].addEventListener('hide.bs.modal', modalHide); // TODO: Corriger
        }
    })
})