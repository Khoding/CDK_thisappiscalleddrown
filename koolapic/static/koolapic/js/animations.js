/**
 * Nécessite :
 * JQuery (Slim supporté)
 * Anime.js
 */
import anime from '../lib/animejs/lib/anime.es.js';

anime({
    targets: '.messages',
    easing: 'easeOutElastic(1, .5)',
    translateY: '10vh',
    duration: 1250,
    opacity: 1,
    direction: 'alternate',
    complete: function (anim) {
        $(".messages").remove()
    }
})