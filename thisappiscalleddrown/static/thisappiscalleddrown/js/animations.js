/**
 * Animations diverses.
 * Nécessite :
 * JQuery (Slim supporté)
 * Anime.js
 */

import anime from '../../vendor/node_modules/animejs/lib/anime.es.js';

anime({
    targets: '#messages',
    easing: 'easeOutElastic(1, .5)',
    translateY: '-10vh',
    duration: 1250,
    opacity: [0, 1],
    direction: 'alternate',
    complete: function (anim) {
        $('#messages').find('.alert').remove()
    }
})