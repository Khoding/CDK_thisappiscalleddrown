/**
 * Permet d'ajouter des alertes depuis le frontend.
 * Nécessite :
 * JQuery (Slim supporté)
 */


/* Anime.js */
import anime from '../../../vendor/node_modules/animejs/lib/anime.es.js'; // Animation

export {alert}

/**
 * Ajoute une alerte avec un message sur la page
 * @param severity string : severité du message
 * @param message string : message
 */
function alert(severity, message) {

    severity = severity.toUpperCase()
    let bootstrapColor = 'light'
    let srOnly = 'Message de sévérité inconnue : '
    let messagesWrapper = $("#messages")[0]

    switch (severity) {
        case 'DEBUG':
            bootstrapColor = 'dark'
            srOnly = 'Message de débogage : '
            break
        case 'INFO':
            bootstrapColor = 'info'
            srOnly = 'Information : '
            break
        case 'SUCCESS':
            bootstrapColor = 'success'
            srOnly = 'Succès : '
            break
        case 'WARNING':
            bootstrapColor = 'warning'
            srOnly = 'Avertissement : '
            break
        case 'ERROR':
            bootstrapColor = 'danger'
            srOnly = 'Erreur : '
            break
    }

    messagesWrapper.innerHTML =
        `<div class="alert alert-dismissable alert-${bootstrapColor} show" role="alert">
            <div class="sr-only">${srOnly}</div>
                ${message}
                <button type="button" class="close" data-dismiss="alert" aria-label="Fermer">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        </div>`

    /* Animation */
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
}

